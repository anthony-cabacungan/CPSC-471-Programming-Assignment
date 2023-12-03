# python cli.py <server machine> <server port>

import socket
import sys
import os

headerSize = 10
clientFolder = "clientFiles/"


# TODO: implement functions
def ftp_get(file_name, control_socket, serverMachine):
    # Sending command to the server
    send_data(control_socket, f"GET {file_name}")
    print(f"Requested file: {file_name}")
    
    # opens a ephemeral port to the server
    data_socket = data_connection(control_socket, serverMachine)
    # Receive file size from the server
    # receive the first 10 bits...the first 10 bits are the file size
    file_size_data = receive_data(data_socket,10)
    print(file_size_data)

    try:
        file_size = int(file_size_data)
        print(f"File size: {file_size}")
    except ValueError:
        print(f"Received invalid file size: {file_size_data}")
        return

    if file_size > 0:
        # Download file <file name> from the server
        content = data_socket.recv(file_size)
        with open(clientFolder + file_name, 'wb') as f:
            f.write(content)
        print(f"Downloaded {file_name}")
    else:
        print("File not found or empty")
    data_socket.close()



def ftp_put(file_name, control_socket, serverMachine):
    send_data(control_socket, f"PUT {file_name}")
    file_path = clientFolder + file_name  # Include the client folder in the path
    print(f"Attempting to upload file from path: {file_path}")  # Debugging info
    # opens a ephemeral port to the server
    data_socket = data_connection(control_socket, serverMachine)
    try:
        with open(clientFolder + file_name, 'r') as f:
            content = f.read()
        
        dataSize = str(len(content))
        while len(dataSize) < 10:
            dataSize = "0" + dataSize
        send_data(data_socket,dataSize)
        send_data(data_socket,content)
    except FileNotFoundError:
        print("file not found")
    data_socket.close()


def ftp_ls(control_socket,server):
    # send command to server
    send_data(control_socket, "LS")

    ephemeral_port = data_connection(control_socket, server)
    # lists files on the server
    print(receive_data(ephemeral_port,1024))
    ephemeral_port.close()


def ftp_quit(sock):
    # disconnects from the server and exits
    send_data(sock, "QUIT")
    sock.close()
    print("Disconnected from server")
    sys.exit()


# Helper functions
def send_data(sock, data):
    sock.sendall(data.encode())


def receive_data(sock,size):
    data = sock.recv(size).decode()
    if len(data) != size:
        print("Missing data")
    return data

# create ephemeral port to the server
def data_connection(sock, serverMachine):
    portNumber = sock.recv(5).decode()

    print(f"Attempting to connect data port at {portNumber}")
    try:
        ephemeralPort = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ephemeralPort.connect((serverMachine, int(portNumber)))
    except:
        print("fail")
    print("connected")
    return(ephemeralPort)


# TODO: input validation / error handling wherever needed
def main():
    if len(sys.argv) != 3:
        print("Usage: python cli.py <server machine> <server port>")
        sys.exit()

    serverMachine = sys.argv[1]
    serverPort = int(sys.argv[2])
    try:
        # create control channel socket
        # Control channel lasts throughout the ftp
        # session and is used to transfer all commands (ls, get, and put) from client to server
        # and all status/error messages from server to client.
        # create data channel socket
        controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("create control socket")

        # create data channel socket
        # dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #created the data socket to early..should be created for each ftp command
        # print("create data socket")                                      

        # DNS lookup to get IP address
        ip = socket.gethostbyname(serverMachine)
        print("get ip", ip)

        controlSocket.connect((serverMachine, serverPort))
         # dataSocket.connect((serverMachine, serverPort))
        print("Connected to server.")

        # create control channel socket
        # Control channel lasts throughout the ftp
        # session and is used to transfer all commands (ls, get, and put) from client to server
        # and all status/error messages from server to client.
        # controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print("create control socket")

        # create data channel socket 
        # dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print("create data socket")

        # connect control
        # controlSocket.connect((ip, serverPort))
        # print("connect control socket")

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
        print("ftp ls               : lists files on the server")
        print("ftp quit             : disconnects from the server and exits")
        print()

        # generate ephemeral port for data socket
        while True:
            command = input("Enter a command: ")
            cmd_parts = command.split(maxsplit=2)  # Split the command into parts
            if len(cmd_parts) < 2:
                print("Invalid command format")
                continue

            cmd_action = cmd_parts[1]  # The action (get, put, ls, quit)
            file_name = cmd_parts[2] if len(cmd_parts) > 2 else None  # The file name if present


            # when an ftp command is run a ephemeral port is open than closed when trasfer is over
            if cmd_parts[0] == "ftp":
                if cmd_action == "get" and file_name:
                    ftp_get(file_name, controlSocket, serverMachine)
                elif cmd_action == "put" and file_name:
                    ftp_put(file_name, controlSocket, serverMachine)
                elif cmd_action == "ls":
                    ftp_ls(controlSocket, serverMachine)
                elif cmd_action == "quit":
                    send_data(controlSocket, "QUIT")
                    break
                else:
                    print("Invalid command")
            else:
                print("Invalid command")
    finally:
        controlSocket.close()


if __name__ == "__main__":
    main()
