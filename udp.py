import threading
import socket
import messages

class listen_udp(threading.Thread):
    def __init__(self, chatter_info:str):
        threading.Thread.__init__(self)
        chatter_info = chatter_info.split(' ')
        self.screen_name = chatter_info[0]
        self.ip = chatter_info[1]
        self.port = chatter_info[2]

    def run(self):
        print('udp run', self.screen_name, self.ip, self.port)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.ip, int(self.port)))
        data = b''
        while True:
            buffer = s.recv(1024)
            data += buffer
            if b'\n' in buffer:
                tmp = data.decode('utf-8')
                tmp = tmp.replace("MESG ", "")
                print(tmp)
                data = b''

def sendMessage(screen_name:str, person:str, msg:str):
    person_split = person.split(' ')
    ip = person_split[1]
    port = person_split[2]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(messages.mesg_message(screen_name,msg),(ip,int(port)))
    s.close()
