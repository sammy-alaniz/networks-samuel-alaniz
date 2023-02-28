import threading

# reference implementation https://superfastpython.com/thread-safe-list/

class ClientData:
    def __init__(self) -> None:
        self._client_list = []
        self._lock = threading.Lock()

    def append(self, value:bytes):
        with self._lock:
            self._client_list.append(value)

    def remove(self, value:bytes):
        with self._lock:
            self._client_list.remove(value)

    def contains(self, value:bytes) -> bool:
        with self._lock:
            if value in self._client_list:
                return True
            else:
                return False

    