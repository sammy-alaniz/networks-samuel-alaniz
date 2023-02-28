import sys
import tcp
import data

if "__main__" == __name__ :
    print("Server has started!")

    listening_tcp_port = str(sys.argv[1])

    #THREAD SAFE DATA MODEL
    client_data = data.ClientData()


    #TCP SERVER
    inital_tcp_connection = tcp.tcp_init_thread(listening_tcp_port, client_data)
    inital_tcp_connection.start()

    #UDP SENDER


    #Have all threads join
    inital_tcp_connection.join()