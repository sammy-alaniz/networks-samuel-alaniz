
def hello_message(screen_name:str, ip:str, port:str) -> str:
    rtn = 'HELO ' + screen_name + ' ' + ip + ' ' + port + '\n'
    return rtn.encode('utf-8')