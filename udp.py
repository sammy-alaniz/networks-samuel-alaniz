import threading
import socket
import messages
import queue

class listen_udp(threading.Thread):
    def __init__(self, chatter_info:str, people:queue):
        threading.Thread.__init__(self)
        chatter_info = chatter_info.split(' ')
        self.screen_name = chatter_info[0]
        self.ip = chatter_info[1]
        self.port = chatter_info[2]
        self.people = people
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip, int(self.port)))

    def run(self):
        print('udp run', self.screen_name, self.ip, self.port)
        data = b''
        while True:
            buffer = self.socket.recv(1024)
            data += buffer
            if b'\n' in buffer:
                self.parse(data)
                data = b''

    def parse(self, data: bytes):
        if b'JOIN ' in data:
            self.join(data)
        if b'MESG ' in data:
            self.mesg(data)
        if b'EXIT ' in data:
            self.exit(data)

    def exit(self, data:bytes):
        print('exit')
        tmp = data.decode('utf-8')
        tmp = tmp.replace('EXIT ','')
        tmp = tmp.replace('\n','')
        for i in range(self.people.qsize()):
            person = self.people.get()
            if tmp in person:
                continue
            self.people.put(person)
        print('Left the chat room : ', tmp)
        self._print_people()

    def join(self, data: bytes):
        tmp = data.decode('utf-8')
        tmp = tmp.replace('JOIN ','')
        tmp = tmp.replace('\n','')
        print('User has joined', tmp)
        self.people.put(tmp)
        self._print_people()

    def mesg(self, data: bytes):
        tmp = data.decode('utf-8')
        tmp = tmp.replace("MESG ", "")
        print(tmp)
    
    def _print_people(self):
        for person in list(self.people.queue):
            print(person)



def sendMessage(screen_name:str, person:str, msg:str):
    person_split = person.split(' ')
    ip = person_split[1]
    port = person_split[2]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(messages.mesg_message(screen_name,msg),(ip,int(port)))
    s.close()
