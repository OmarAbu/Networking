#Omar Abu-Rmaileh
import logging
import socket
import sys
from urllib import request, response
from urllib.parse import urlparse
import requests as reqs 
import re

def retrieve_url(url):
    """
    return bytes of the body of the document at url
    """

    
    protocol_version = " HTTP/1.1"
   

    t=url.split('/')
    

   
 
  
    host=t[2]

    
    
    path=''
    #print(t)
    if(len(t)<=3):
        path+='/'
    for index in t[3:]:
        path+='/'+index
    #port
    st=host.split(":", 1)
    if(st==None or len(st)==1):
        port=80
    else:
        port=int(st[1])
    


    

   
 
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientsocket.connect((host, port))
        request =  ("GET " +path+
                protocol_version+"\r\nHost:" +host +
                "\r\nConnection: close\r\n\r\n")
        clientsocket.send(request.encode())
    except socket.error:
        return None

 



    packets=[]
    
    while True:
        try:
            test=clientsocket.recv(4096)
            if test :
                packets.append(test)
                test=None
                continue
            else:
                break
        
          
        except socket.error:
            return None
    #test=None
    result=b"".join(packets)
    test=result
    
    if(test.__contains__(b"200") ==True):
        new_data = test.split(b"\r\n\r\n", 1)
        #print(new_data[1])
        return new_data[1]
    elif test.__contains__(b"301")==True:

      
            
            res=test.split(b"The document has moved")
    
           # print(res[1])
            #find the new url
            m=re.findall(b'"([^"]*)"', res[1])
      
            return   retrieve_url(m[0].decode())
    else:
            print("nothing to retrieve")
            return None

       
       


    

    

        

   



if __name__ == "__main__":
    
    sys.stdout.buffer.write(retrieve_url(sys.argv[1])) # pylint: disable=no-member