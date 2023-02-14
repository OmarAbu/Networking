
from os import popen
import os
from socket import *
import ssl
import subprocess 
from email.mime.text import MIMEText
import os
import sys
import re
import tempfile
correct="full path for correct.txt"
wrong_d="full path for wrong_domain.txt"
wrong_f="full path for wrong_format.txt"
wrong_r="full path for wrong_recipient.txt"

s=open(correct, 'r') 
contents=s.read()

print("THIS PORTION IS Obtaining emails\n")
    #findthe From email and lst[1] is the to Email
lst = re.findall('[^,;\s]+@[^,;\s]+', contents)     
print(lst[0] + "From email address")
print(lst[1]+  "To email address")

if(lst[1]!="<hamed.rezaei@zoho.com>"):
    print("wrong recipient")
print("---------------------------------------------")

print("THIS PORTION IS CHECKING EMAIL FORMAT\n")

def check(email):
    email= email.strip("<")
    email=email.strip(">")
    
    regex = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if(re.match(regex, email)):
       return print(email + " is a Valid Email")
    else:
        return print(email + " is an Invalid Email") 

check(lst[0])
check(lst[1])
print("---------------------------------------------")

print("this portion is recieving the domain and the address of that domain \n")
#get domain  name from terminal
dom_name= lst[1][lst[1].index('@') + 1 : -1]


print("this is the domain name " + dom_name)

args= "dig mx "+dom_name+  " +short"
loc3=subprocess.getoutput(args)
res=loc3.split()

#if res[1]is empty than there is no server list
if not res:
    print("Incorrect domain ")
else:
    print(res[1])

print("---------------------------------------------")

print("this portion is to get the subject of the email\n")
#method to get subject
def Subject():
    with open(correct) as f:
        datafile = f.readlines()

    for line in datafile:

        if 'Subject:' in line:
            line.split()
            return line.strip('Subject:')
      
    return False  # Because you finished the search without finding
print(Subject())

print("---------------------------------------------")
print("this portion is to get the messae of the txt file\n")
#to find the msg
def getMsg():
    with open(correct) as f:
        mzg= [line.strip() for line in f.readlines()]
    return mzg[len(mzg)-1]

print(getMsg())


print("---------------------------------------------")





#lst[0] goes here
fEmail= lst[0]
#lst[1] goes here
tEmail = "<figyzyfo@getnada.com>"

#res[1]= server of the domain function goes here
server="testmail.getnada.com."


Port = 25  # SMTP uses port 25
cSocket = socket(AF_INET, SOCK_STREAM)

cSocket.connect((server,Port))  
conn= cSocket.recv(1024).decode()
print(conn)
if '220' != conn[:3]:
    print('220 reply not received from server.')

heloCommand = 'HELO Alice\r\n'
cSocket.send(heloCommand.encode()) 
yo = cSocket.recv(1024).decode()
print(yo)
if '250' != yo[:3]:
    print('250 reply not received from server.')


From=f"MAIL FROM: {fEmail} \r\n"
cSocket.sendall(From.encode())
recFrom = cSocket.recv(1024).decode()
print(recFrom)
if '250' != recFrom[:3]:
    print('250 reply not received from server')


# Then, the SMTP client sends one or more RCPT (short for recipient) commands in the format of RCPT TO: < recipient address >.
# Send the RCPT TO command, including the email address of the recipient, and return the status code 250
#clientSocket.sendall(('RCPT TO: <' + toAddress + '>\r\n').encode())
rcpt_to = f"RCPT TO: {tEmail} \r\n"
cSocket.send(rcpt_to.encode())
recTo = cSocket.recv(1024).decode()
#recvTo = clientSocket.recv(1024).decode()  # Note that UDP uses sendto and recvfrom
print(recTo)
if '250' != recTo[:3]:
    print('250 reply not received from server')


cSocket.sendall(('DATA\r\n').encode())
Data = cSocket.recv(1024).decode()
print(Data)
if '354' != Data[:3]:
    print('354 reply not received from server')

# Edit email information and send data
subject = Subject()
message=getMsg()
endMsg = "\r\n.\r\n"

output = 'from:' + fEmail + '\r\n'
output+= 'to:' + tEmail + '\r\n'
output += 'subject:' + subject + '\r\n'
output += '\r\n' + message

cSocket.sendall(output.encode())


# With "." end. Request successful return 250
cSocket.sendall(endMsg.encode())
recvEnd = cSocket.recv(1024).decode()
print(recvEnd)
if '250' != recvEnd[:3]:
    print('250 reply not received from server')

# Send the "QUIT" command to disconnect from the mail server
cSocket.sendall('QUIT\r\n'.encode())

cSocket.close()
