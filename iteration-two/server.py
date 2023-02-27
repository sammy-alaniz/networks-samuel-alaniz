import sys
import tcp

if "__main__" == __name__ :
    print("Server has started!")

    listening_tcp_port = str(sys.argv[1])

    #TCP SERVER
    inital_tcp_connection = tcp.listen_tcp(listening_tcp_port)
    inital_tcp_connection.start()

    #UDP SENDER


    #Have all threads join
    inital_tcp_connection.join()