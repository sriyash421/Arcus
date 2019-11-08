import socket
import select
import sys
# from thread import *
from constants import *
import random

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)



IP_address = SERVER_IP	
Port = PORT

server.bind((IP_address, Port))

server.listen(5)

print ("Server_Running_Successfully")

list_of_clients=[]
list_of_addr=[]
count=0


def remove(connection): 

    if connection in list_of_clients: 

        list_of_clients.remove(connection)


while True:
    conn,addr=server.accept()
    list_of_clients.append(conn)
    list_of_addr.append(addr)
    count+=1
    print (addr[0] + " :connceted :User No. %d"%(count))
    if count ==2:
        status = str.encode("Success")
        list_of_clients[0].send(status)
        list_of_clients[1].send(status)
        break


while True:
    output_0=list_of_clients[1].recv(2048)
    output_1=list_of_clients[0].recv(2048)
    print("{}\t{}".format(output_1,output_0))
    list_of_clients[0].send(output_0)
    list_of_clients[1].send(output_1)





conn.close()
server.close()					