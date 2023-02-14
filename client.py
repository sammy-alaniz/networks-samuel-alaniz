import socket
import messages
import tcp
import queue
import time

if __name__ == "__main__":
    server_ip = "10.37.129.3"
    server_port = "61616"
    screen_name = 'Google'
    people = queue.Queue()
    tcp_thread = tcp.tcp('Young', server_ip, server_port, people)
    tcp_thread.start()
    