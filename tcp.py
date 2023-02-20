import threading
import queue 
import socket
import messages
import udp
import random
import sys

class tcp(threading.Thread):
    def __init__(self, screen_name:str ,ip:str, port:str ,people:queue):
        threading.Thread.__init__(self)
        self.ip = ip
        self.server_port = port
        client_port = str(random.randint(50000,60000))
        self.client_port = client_port
        self.people = people
        self.screen_name = screen_name
        self.keep_going = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, int(self.server_port)))
        self.udp_thread = None

    def run(self):
        client_ip = self.socket.getsockname()[0]
        self.socket.sendall(messages.hello_message(self.screen_name, client_ip, self.client_port))
        data = b''
        try:
            while self.keep_going:
                buffer = self.socket.recv(1024)
                data += buffer
                if b'\n' in buffer:
                    self.parse(data)
                    data = b''
        except OSError as e:
            sys.exit()

    def parse(self, data: bytes):
        if b'ACPT' in data:
            self.accept(data)
        if b'RJCT' in data:
            self.rejected(data)

    def accept(self, data:bytes):
        str_data = data.decode('utf-8')
        str_data = str_data.replace('ACPT ', '')
        str_data = str_data.replace('\n','')
        parts = str_data.split(':')
        for part in parts:
            if self.screen_name in part:
                self.udp_thread = udp.listen_udp(part,self.people,self, self.screen_name)
                self.udp_thread.start()
            self.people.put(part)
        self._print_chatroom()

    def rejected(self, data:bytes):
        str_data = data.decode('utf-8')
        str_data = str_data.replace('RJCT ', '')
        str_data = str_data.replace('\n','')
        print('This name is already in use! : ', str_data)
        self.end_tcp()

    def send_exit(self):
        if self.keep_going:
            self.socket.sendall(b'EXIT\n')

    def end_tcp(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.keep_going = False
        sys.exit()

    def _print_chatroom(self):
        print('In chat room')
        for person in list(self.people.queue):
            print(person)
        



