import socket
import os

connections = []
totalConnections = 0

class Client(object):
    def __init__(self,data, files, signal):
        self.data = data 
        self.signal = signal
  
    def downloadFiles(files):
        """
        download files
        :params files: list of files 
        """
        downloadDir = os.getcwd()
        for f in files: 
            downloadDir += f 
        with open (downloadDir, 'r') as f:
             print(f.read(8)," ... ")  


def newConnection(sock):
    """
    creates new connection between client and server
    :params data: socket
    """
    while True:
        print('Waiting for a connection ... ')
        clientSocket, clientAddress = sock.accept()
        bracketsPairs = clientSocket.recv(1024) 
        print('Connected by', clientAddress)
        try:
            if int(bracketsPairs) == 2:
               data = clientSocket.recv(1024)
               portAndFiles = extractPortAndFiles(data)               
               msg = str(portAndFiles[0])+', '+' , '.join(portAndFiles[1])+', '+str(clientAddress[1])+', '+clientAddress[0]
               connections.append(Client(msg, portAndFiles[1], True))       
               bracketsPairs = clientSocket.recv(1024)

            if int(bracketsPairs) == 1:
               data = clientSocket.recv(1024)
               searchedData = search(data)
               searchedData += '\n'
               clientSocket.send(searchedData.encode('utf-8'))        
               
        finally:
            print('Closing current connection')
            clientSocket.close()

 
def extractPortAndFiles(data):
    """
    split port and files names from brackets format and put into list
    :params data: string [port][files]
    :return: list with port and files   
    """
    string = ((str(data).replace('][','#')).replace(']','#')).replace('[','#')
    splitedData = [s for s in list(string.split('#')) if s.isdigit() or '.' in s] 
    return [splitedData[0], splitedData[1].split(',')]


def search(data):
    """
    search files, id, ports etc. by the data param
    :params data: user input
    :return: all data that consist input    
    """ 
    data = (((str(data).replace('[','')).replace(']','') ).replace('b','')).replace("'","")
    substringList = [data[i: j] for i in range(len(data)) for j in range(i + 1, len(data) + 1)]
    msg = '' 
    for c in connections:
      stringsList = c.data.strip().split(', ')
      for item  in stringsList:
        for sub in substringList: 
          if str(sub) in str(item) or item[0].isdigit():
             if not str(item) in msg:
                msg = '['+str(item)+']'+msg
    return  msg  


if __name__ == "__main__":
    #Get host and port
    host = input("Host: ") 
    port = int(input("Port: "))

    #Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    newConnection(sock)



