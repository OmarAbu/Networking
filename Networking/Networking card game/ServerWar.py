from asyncio import sleep, wait
from colorsys import ONE_SIXTH
from copyreg import pickle
from glob import escape
import random
import socket
import sys
import struct
from tkinter import commondialog
    
def split_deck():
    cards=list(range(0,52))
    yours = random.sample(cards, 26)
    opp = [i for i in cards if i not in yours]
    random.shuffle(opp)
    return yours, opp
  
def compare_cards(card1, card2):
    """
    TODO: Given an integer card representation, return -1 for card1 < card2,
    0 for card1 = card2, and 1 for card1 > card2
    """
    if (card1 % 13) > (card2 % 13):
        return 0
    elif (card1 % 13) == (card2 % 13):
        return 1
    else:
        return 2
port = int(sys.argv[1])
deck=split_deck()
d1 =deck[0]
d2 =deck[1]
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', port))
    # s.sendall(b"Hello, world")
    # data = s.recv(1024)
    # print(f"Received {data!r}")
s.listen(2)
list=[]
#this will be true unless there is two clients
while True:
        conn, addr = s.accept()
   
        print(f"Connected by {addr}")
                
                #this will recieve stuff from each client 
                #data = conn.recv(1024)
                
                
        list.append(conn)
        if(len(list)==2):
            break
#s.close()
print("exit loop")
p1=list[0]
p2=list[1]
print("both connected")
#game start message
p1.send(struct.pack('b',1))
p2.send(struct.pack('b', 1))
#sees if the players are ready to play
t1=struct.unpack('B',p1.recv(1024))
t2=struct.unpack('B',p2.recv(1024))
#check to see if players both sent the one value
if t1.__contains__(0)==False or t2.__contains__(0)==False:
    print("one player does not want to play")
    p1.close()
    p2.close()
else:
    print("both players ready to play")
    t1=None
    t2=None
    
    # d1=np.arange(1,26).tolist()
    # d2=np.arange(27,52).tolist()
    # print(d1)
   
    # p1.send(data1)
    # p2.send(data2)
    p1.send(struct.pack('26B', *d1))
    p2.send(struct.pack('26B', *d2))
    p2Count=0
    p1Count=0
    tie=0
    ttlCount=0
    
    while ttlCount<27:
        
        p1Card=struct.unpack('2b',p1.recv(1024))
        p2Card=struct.unpack('2b',p2.recv(1024))
        if(p1Card[0]==2 and p2Card[0]==2):
    
            if compare_cards(p1Card[1],p2Card[1])==0:
                    p1Count=p1Count+1
                    print("player 1 has won this round his score is", p1Count, 
"player 2 score is ", p2Count, " tie ",tie)
                    p1.send(struct.pack('B', 0))
                    p2.send(struct.pack('B',2))
            elif compare_cards(p1Card[1],p2Card[1])==2:
                    
                    p2Count=p2Count+1
                    print("player 2 has won this round his score is", p2Count, 
"player 1 score is ", p1Count," tie ",tie)
                    p1.send(struct.pack('B', 2))
                    p2.send(struct.pack('B',0))
                    
            else:
                    print("there is a tie " , tie)
                    tie=tie+1
                    p1.send(struct.pack('B', 1))
                    p2.send(struct.pack('B',1))
        else:
        
            if compare_cards(p1Card[1],p2Card[1])==0:
                    p1Count=p1Count+1
                
            elif compare_cards(p1Card[1],p2Card[1])==2:
                    
                    p2Count=p2Count+1
                    print("player 2 has won this round his score is", p2Count, 
"player 1 score is ", p1Count," tie ",tie)
                
                    
            else:
                    print("there is a tie " , tie)
                    tie=tie+1
        ttlCount=ttlCount+1
        p1Card=None
        p2Card=None
if(p1Count>p2Count):
    p1.sendall(b'player one won!')
    p2.sendall(b'player two lost')
elif p2Count>p1Count:
    p2.sendall(b'player two won!')
    p1.sendall(b'player one lost')
else:
    p1.sendall(b'player one and player two tied')
    p2.sendall(b'player 1 and player 2 tied')
p1.close()
p2.close()
