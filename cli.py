# python cli.py <server machine> <server port>

import socket
import sys
import os

headerSize = 10
clientFolder = "clientFiles/"


# TODO: implement functions
def ftp_get(file_name, control_socket, data_socket):
    # Sending command to the server
    send_data(control_socket, f"GET {file_name}")
    print(f"Requested file: {file_name}")

    # Receive file size from the server
    # receive the first 10 bits...the first 10 bits are the file size
    file_size_data = receive_data(data_socket,10)

    try:
        file_size = int(file_size_data)
        print(f"File size: {file_size}")
    except ValueError:
        print(f"Received invalid file size: {file_size_data}")
        return

    if file_size > 0:
        # Download file <file name> from the server
        content = data_socket.recv(file_size)
        with open(file_name, 'wb') as f:
            f.write(content)
        print(f"Downloaded {file_name}")
    else:
        print("File not found or empty")



def ftp_put(file_name, control_socket, data_socket):
    file_path = clientFolder + file_name  # Include the client folder in the path
    print(f"Attempting to upload file from path: {file_path}")  # Debugging info

    try:
        with open(file_name, 'rb') as f:
            content = f.read()
        # send data
        send_data(control_socket, f"PUT {file_name}")
        # Makes sure the dataSize is 10 bits
        dataSizeStr = str(len(content))
        while len(dataSizeStr) < 10:
            dataSizeStr = "0" + dataSizeStr
        fileData = dataSizeStr + content
        send_data(data_socket, dataSizeStr)
        # uploads file <file name> to the server
        data_socket.sendall(fileData.encode())
        print(receive_data(data_socket))
    except FileNotFoundError:
        print("File not found")


def ftp_ls(control_socket, data_socket):
    # send command to server
    send_data(control_socket, "LS")

    # lists files on the server
    print(receive_data(data_socket))


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
    if data == "":
        print("Received empty data")
    return data

# create ephemeral port to the server
def create_ephemeral_Port(serverMachine, sock):
    sock.bind(('',0))
    sock.listen(1)
    portNumber = sock.getsockname()[1]
    print("ephermeral port is : " + portNumber)
    ephemeralPort = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ephemeralPort.connect((serverMachine, portNumber))
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
                    dataSocket = create_ephemeral_Port(serverMachine, controlSocket)
                    ftp_get(file_name, controlSocket, dataSocket)
                    dataSocket.close()
                elif cmd_action == "put" and file_name:
                    dataSocket = create_ephemeral_Port(serverMachine, controlSocket)
                    ftp_put(file_name, controlSocket, dataSocket)
                    dataSocket.close()
                elif cmd_action == "ls":
                    dataSocket = create_ephemeral_Port(serverMachine, controlSocket)
                    ftp_ls(controlSocket)
                    dataSocket.close()
                elif cmd_action == "quit":
                    send_data(controlSocket, "QUIT")
                    break
                else:
                    print("Invalid command")
            else:
                print("Invalid command")
    finally:
        controlSocket.close()
        dataSocket.close()


if __name__ == "__main__":
    main()
