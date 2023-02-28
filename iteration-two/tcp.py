import threading
import socket
import messages
import sys
import time
import data

class tcp_init_thread(threading.Thread):
    def __init__(self, tcp_listening_port, client_data:data.ClientData):
        threading.Thread.__init__(self)
        self.tcp_listening_port = tcp_listening_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = self.socket.getsockname()[0]
        self.socket.bind((self.server_ip, int(self.tcp_listening_port)))
        self.client_data = client_data
        
    def run(self):
        while True:
                self.socket.listen()
                conn, addr = self.socket.accept()
                print(type(conn))
                client_thread = tcp_client_thread(conn,self.client_data)
                client_thread.start()




class tcp_client_thread(threading.Thread):
    def __init__(self, connection:socket, cleint_data:data.ClientData):
        threading.Thread.__init__(self)
        self.sock = connection
        self.hello_data = None
        self.cleint_data = cleint_data

    def run(self):
        data = b''
        try:
            while True:
                time.sleep(2)
                #self._print()
                buffer = self.sock.recv(1024)
                data += buffer
                if b'\n' in buffer:
                    self.parse(data)
                    data = b''
                if b'' in buffer:
                    self.shutdown()
        except OSError as e:
            sys.exit()

    def parse(self, msg:bytes):
        if b'HELO ' in msg:
            self.hello(msg)

    def hello(self,msg:bytes):
        self.hello_data = messages.parse_hello_message(msg)
        if self.cleint_data.contains(msg):
            self.send_reject_message()
        else:
            self.cleint_data.append(msg)
    
    def send_reject_message(self):
        print('send reject message')

        print('screen name', self.hello_data.screen_name)
        print('ip ', self.hello_data.ip)
        print('port ', self.hello_data.port)
    
    def _print(self):
        if self.hello_data != None:
            print('screen name', self.hello_data.screen_name)
            print('ip ', self.hello_data.ip)
            print('port ', self.hello_data.port)

    def shutdown(self):
        print('Shuting Down!')
        self._print()
        sys.exit()
        






# this might better fit a udp thread
class udp_client_thread(threading.Thread):
    def __init__(self, hello_message:bytes):
        threading.Thread.__init__(self)
        self.hello_data = messages.parse_hello_message(hello_message)
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
