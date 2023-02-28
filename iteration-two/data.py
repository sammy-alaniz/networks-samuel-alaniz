import threading

# reference implementation https://superfastpython.com/thread-safe-list/

class client:
    def __init__(self, screen_name:str, ip:str, port:str) -> None:
        self.screen_name = screen_name
        self.ip = ip
        self.port = port


class ClientData:
    def __init__(self) -> None:
        self._client_list = []
        self._lock = threading.Lock()

    def append(self, screen_name:str, ip:str, port:str):
        with self._lock:
            tmp = client(screen_name,ip,port)
            self._client_list.append(tmp)

    def remove(self, screen_name:str):
        with self._lock:
            for i in self._client_list:
                if i.screen_name == screen_name:
                    self._client_list.remove(i)

    def contains(self, screen_name:str) -> bool:
        with self._lock:
            for i in self._client_list:
                if i.screen_name == screen_name:
                    return True
            return False

    