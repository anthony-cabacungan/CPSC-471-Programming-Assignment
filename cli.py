# python cli.py <server machine> <server port>

import socket
import sys

headerSize = 10
clientFolder = "clientFiles/"

# TODO: implement functions
def ftp_get(file_name, control_socket, data_socket):
    # downloads file <file name> from the server

    # create ephemeral port for the data socket
    dataPort = ephemeral_Port(data_socket)
   
    # sending command to the server
    command = "get"
    send_data(control_socket,command)

    # send requested file name 
    send_data(control_socket, file_name)
    
    # receive size of data from server
    dataSize = int(receive_data(dataPort, headerSize))

    # reveive data from the server
    data = receive_data(dataPort, dataSize)
    
    # Create file with received data
    fileData = open(clientFolder + file_name, "x")
    fileData.write(data)
    print("The number of bytes that got transferred: " + str(dataSize))
    dataPort.close()
    return 0

def ftp_put(file_name, control_socket, data_socket):
    # uploads file <file name> to the server
    command = "put"
    send_data(control_socket, command)
    try:
        sendFile = open(clientFolder + file_name, "r")
        file = sendFile.read()
        fileSize = len(file)
    except Exception as e:
        print(e)
        return
    # create ephemeral port for the data socket
    dataPort = ephemeral_Port(data_socket)
    
    # adjusted data to fit fixed header size
    fileNameSize = len(file_name)
    fileSize = str(dataSize)
    while len(dataSize) < 10:
        dataSize = "0" + dataSize

    while len(file_name) < 10:
        file_name = "0" + file_name
    
    # add headers to data
    data = fileName + fileSize + file
    
    #send data
    send_data(dataPort,data)
    print(file_name + " upload successful.")
    print("Bytes sent: " + str(len(data)))

    sendFile.close()
    dataPort.close()

def ftp_ls(control_socket, data_socket):
    # lists files on the server
    # send command to server
    command = "ls"
    send_data(control_socket, command)
    
    # create ephemeral port for the data socket
    dataPort = ephemeral_Port(data_socket)

    #receive size of data from server
    dataSize = int(receive_data(dataPort, headerSize))

    #receive list of files
    response = receive_data(dataPort, dataSize)

    print(response)
    dataPort.close()

def ftp_quit(controlSocket, dataSocket):
    # disconnects from the server and exits
    controlSocket.close()
    dataSocket.close()
    print("Disconnected from server")
    sys.exit()

# Helper functions
# Send data until all bytes sent
def send_data(socket, data):
    data = data.encode("utf-8")
    sentBytes = 0
    while len(data) > sentBytes:
        sentBytes += socket.send(data[sentBytes:])

# create ephemeral port for the data socket
def ephemeral_Port(data_socket):
    data_socket.bind(('',0))
    data_socket.listen(1)
    dataPort = data_socket.getsockname()[1]
    return(dataPort)

# keep receiving data until all bytes are received
def receive_data(dataPort, dataSize):
    data = ""
    while True:
        data = dataPort.recv(dataSize).decode("utf-8")
        if len(data) == dataSize:
            print("File received")
            break
        # The other side has closed the socket
        if not data:
            print("Failed to receive data")
            break
    return data

if __name__ == "__main__":
    # TODO: input validation / error handling wherever needed

    if len(sys.argv) != 3:
        print("Usage: python cli.py <server machine> <server port>")
        sys.exit()
    
    serverMachine = sys.argv[1] 
    serverPort = int(sys.argv[2])

    try:
        # DNS lookup to get IP address
        ip = socket.gethostbyname(serverMachine)
        print("get ip")

        # create control channel socket
            # Control channel lasts throughout the ftp
            # session and is used to transfer all commands (ls, get, and put) from client to server 
            # and all status/error messages from server to client.
        controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("create control socket")

        # create data channel socket 
        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("create data socket")

        # connect control
        controlSocket.connect((ip, serverPort))
        print("connect control socket")

        # Upon connecting to the server, the client prints out ftp>, which allows the user to execute
        # the following commands.
            # ftp> get <file name> (downloads file <file name> from the server)
            # ftp> put <filename> (uploads file <file name> to the server)
            # ftp> ls(lists files on theserver)
            # ftp> quit (disconnects from the server and exits)
        print()
        print("Execute one of the following commands: ")
        print()
        print("ftp get <file name>  : downloads file <file name> from the server")
        print("ftp put <file name>  : uploads file <file name> to the server")
        print("ftp ls <file name>   : lists files on the server")
        print("ftp quit <file name> : disconnects from the server and exits")
        print()


        # generate ephemeral port for data socket
        while True:
            userInput = input("Enter a command: ")
            arguments = userInput.split()
            if arguments[0] == "ftp":
                if arguments[1] == "get":
                    fileName = arguments[2]
                    res = ftp_get(fileName, controlSocket, dataSocket)
                    print(res)
                elif arguments[1] == "put":
                    fileName = arguments[2]
                    res = ftp_put(fileName, controlSocket, dataSocket)
                    print(res)
                elif arguments[1] == "ls":
                    res = ftp_ls(controlSocket, dataSocket)
                    print(res)
                elif arguments[1] == "quit":
                    ftp_quit(controlSocket, dataSocket)
                    break
            else:
                print("Not a valid command")
                print()
    except:
        print("Cannot connect to server")