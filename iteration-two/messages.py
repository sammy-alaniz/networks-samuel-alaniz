
def hello_message(screen_name:str, ip:str, port:str) -> str:
    rtn = 'HELO ' + screen_name + ' ' + ip + ' ' + port + '\n'
    return rtn.encode('utf-8')

def reject_message(screen_name:str) -> str:
    rtn = 'RJCT ' + screen_name + '\n'
    return rtn.encode('utf-8')

class parse_hello_message:
    def __init__(self, msg:bytes) -> None:
        self.original_msg = msg
        str_data = msg.decode('utf-8')
        str_data = str_data.replace('HELO ','')
        str_data = str_data.replace('\n','')
        parts = str_data.split(' ')
        self.screen_name = parts[0]
        self.ip = parts[1]
        self.port = parts[2]

