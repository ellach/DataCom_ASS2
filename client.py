import socket
import glob, os


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest_ip = input("Host: ") 
dest_port = int(input("Port: "))
sock.connect((dest_ip, dest_port))


def sendListOfFiles():
    """
    send list of files and port to server 
    """
    try:
        msg, files = '', []
        for file in glob.glob("*.*"):  
          with open (file, 'rb') as f:
             files.append(f.name)
        msg = '['+str(dest_port)+']'+'['+','.join(files)+']'
        bracketsPairs = str(countMatchingBrackets(msg))
        sock.sendall(bracketsPairs.encode('utf-8'))  
        print('Sending message ... "%s"' % msg )
        sock.sendall(msg.encode('utf-8'))
    except:
        print('Message not sent')
        sock.close()  


def doSearch():
    """
    send search params to server
    """
    try:
        searchParam = input('Enter search parameter: ')
        msg = '[' + searchParam + ']'
        bracketsPairs = str(countMatchingBrackets(msg))
        sock.sendall(bracketsPairs.encode('utf-8'))  
        print('Sending message ... "%s"' % msg )
        sock.sendall(msg.encode('utf-8'))
        data = sock.recv(1024)
        print('Received data:  "%s"' % data) 
    finally:
        print('Closing socket ...')
        sock.close()    


def countMatchingBrackets(data):
    """
    count how match Brackets in string 
    :params data: string
    :return: number of Brackets pairs
    """
    stack = []  
    pairs = 0
    for c in str(data):
      if c == '[':
         stack.append(c)
      elif c == ']':
         if len(stack) == 0:
            pass  
         else:
             stack.pop()
             pairs += 1
    return pairs


def main(): 

    sendListOfFiles()
    userChoise=int(input("Choose (1/0): "))
    if userChoise == 1:
       print("Do Search ...") 
       doSearch()  
 
main()





