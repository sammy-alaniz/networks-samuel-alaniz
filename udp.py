import threading
import socket

class peer_udp(threading.Thread):
    def __init__(self, chatter_info:str):
        threading.Thread.__init__(self)
        chatter_info = chatter_info.split(' ')
        self.screen_name = chatter_info[0]
        self.ip = chatter_info[1]
        self.port = chatter_info[2]

    def run(self):
        print('udp run', self.screen_name, self.ip, self.port)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #s.bind((self.ip, int(self.port)))
        data = b''
        while True:
            buffer = s.recv(1024)
            print(buffer)
            data += buffer
            if b'\n' in buffer:
                print('eom')
                print(data.decode('utf-8'))
                data = b''

