import threading
import socket

class listen_tcp(threading.Thread):
    def __init__(self, tcp_listening_port):
        threading.Thread.__init__(self)
        self.tcp_listening_port = tcp_listening_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = self.socket.getsockname()[0]

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.server_ip, int(self.tcp_listening_port)))
            s.listen()
            conn, addr = s.accept()

            #This next section should spin off onto it's own thread
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    #conn.sendall(data)
                    print(data)


def send_message(msg:bytes, port:str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = s.getsockname()[0]
    s.connect((ip,int(port)))
    s.sendall(msg)
    s.close()
