
def hello_message(screen_name:str, ip:str, port:str) -> str:
    rtn = 'HELO ' + screen_name + ' ' + ip + ' ' + port + '\n'
    return rtn.encode('utf-8')

def mesg_message(screen_name:str, message:str)-> str:
    rtn = 'MESG ' + screen_name + ': ' + message + '\n'
    return rtn.encode('utf-8')