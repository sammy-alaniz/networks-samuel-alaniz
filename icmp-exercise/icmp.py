from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    while count < countTo:
        # thisVal = ord(string[count+1]) * 256 + ord(string[count])
        thisVal = string[count + 1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + ord(string[len(string) - 1])
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []:  # Timeout
            #return "Request timed out."
            return 0

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
        #icmp_header_bytes = recPacket[20:28] <- print this response
        icmp_payload_bytes = recPacket[28:]

        # convert from 8 byte to time
        timestamp_unpack = struct.unpack('d', icmp_payload_bytes)[0]
        
        rtt = abs(timeReceived - timestamp_unpack)

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            #return "Request timed out."
            return 0
        
        return rtt


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())

    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network  byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str


# Both LISTS and TUPLES consist of a number of objects
# which can be referenced by their position number within the object.

def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type. For more details:
    #    http://sock-raw.org/papers/sock_raw

    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay


def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    delay_max = 0
    delay_min = 0
    delay_arr = []

    packets_sent = 0
    packets_lost = 0
    average_loss = 0

    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    # Send ping requests to a server separated by approximately one second
    while 1:
        delay = doOnePing(dest, timeout)
        packets_sent = packets_sent + 1
        
        # min, max, avg rtt, percentage of packet loss

        if (delay > 0):
            print('\nSeconds : ', delay)
            print('Miliseconds : ', (delay * 1000))
            print('')
            if delay_min == 0:
                delay_min = delay
            delay_max = max(delay_max, delay)
            delay_min = min(delay_min, delay)
            print('Delay Min : ', delay_min)
            print('Delay Max : ', delay_max)
            delay_arr.append(delay)
            average = (sum(delay_arr)/len(delay_arr))
            print('Average RTT for all packets (not including the timeouts) : ', average)



        if (delay == 0):
           print('lost packet')
           packets_lost = packets_lost + 1
           average_loss = (packets_lost/packets_sent)*100
        
        print('\nAverage packet loss percentage %: ', average_loss)

        time.sleep(1)  # one second

    return delay


ping("google.com")