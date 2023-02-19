import tcp
import queue
import udp
import sys

if __name__ == "__main__":
    print(sys.argv)
    screen_name = str(sys.argv[1])
    server_ip = str(sys.argv[2])
    server_port = str(sys.argv[3])
    people = queue.Queue()
    tcp_thread = tcp.tcp(screen_name, server_ip, server_port, people)
    tcp_thread.start()

    loop = True

    while loop:
        try:
           tmp = input()
           for person in list(people.queue):
            udp.sendMessage(screen_name, person,tmp)
        except EOFError:
            print('end of file reached')
            print('tcp keep going', tcp_thread)
            print('udp', tcp_thread.udp_thread)
            tcp_thread.send_exit()
            loop = False


    