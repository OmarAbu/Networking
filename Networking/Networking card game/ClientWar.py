from copyreg import pickle
from os import wait
import socket
import sys
import struct
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = sys.argv[1]
PORT = int(sys.argv[2]) 
client.connect((HOST, PORT))
    
#client.listen()
#while True:
#conn, addr = client.accept()
    #with conn:
        #data = client.recv(1024)
#players just recives ddata so I could make it the first twp parts fo the deck
#client.send(b"from client")
test=(struct.unpack('B',client.recv(1024)))
print("\r\n")
print(test)
if test.__contains__(1)==True:
    #client wanting to start game
    client.send(struct.pack('B', 0))
    test=None
else:
    print("some error with socket")
    #close client if they do not want game
    client.close()
print("ready to recieve deck?")
print("\r\n")
deck=[]
res=struct.unpack('26B',client.recv(1024))
for i in res:
    deck.append(i)
res=None
count=26
while True:
    numToSend=2
    while(count>0):
        #change this to change what to send
      
        client.send(struct.pack('2b',numToSend, deck.pop()))
        
        if(numToSend==2):
            result=struct.unpack('B', client.recv(1024))
            print("\r\n")
            if result[0]==0:
                print("client won ", result[0])
            elif result[0]==2:
                print("client lost ", result[0])
            else:
                print("there was a tie")
        
        result=None
        count=count-1
    break
print("this client finished deck")
winner=b''.join(client.recv(1024))
print(winner)
