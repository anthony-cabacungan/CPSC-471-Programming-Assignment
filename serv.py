# python serv.py <PORTNUMBER>

import socket
import sys

# TODO: input validation / error handling wherever needed

if len(sys.argv) != 2:
    print("Usage: python serv.py <PORTNUMBER>")
    sys.exit()

serverPort = int(sys.argv[1])

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind(('', serverPort))

serverSocket.listen(1)

while 1:
    try: 
        print("Waiting for a connection...")
        clientSock, addr = serverSocket.accept()
        print("Accepted connection")
    except:
        print("Could not connect")

if serverPort:
    # TODO: setup server
    print(serverPort)