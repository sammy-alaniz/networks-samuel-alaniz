import socket
import messages
import tcp
import queue
import time

if __name__ == "__main__":
    server_ip = "192.168.1.171"
    server_port = "61616"
    screen_name = 'Google'
    people = queue.Queue()
    tcp_thread = tcp.tcp(screen_name, server_ip, server_port, people)
    tcp_thread.start()
    