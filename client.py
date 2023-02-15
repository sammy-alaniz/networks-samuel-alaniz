import socket
import messages
import tcp
import queue
import time
import udp

if __name__ == "__main__":
    server_ip = "192.168.1.171"
    server_port = "61616"
    screen_name = 'Google'
    people = queue.Queue()
    tcp_thread = tcp.tcp(screen_name, server_ip, server_port, people)
    tcp_thread.start()

    while True:
        tmp = input()
        for person in list(people.queue):
            udp.sendMessage(screen_name, person,tmp)
    