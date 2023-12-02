# python cli.py <server machine> <server port>

import socket
import sys
import os

headerSize = 10
clientFolder = "clientFiles/"


# TODO: implement functions
def ftp_get(sock, file_name):
    # sending command to the server
    send_data(sock, f"GET {file_name}")
    # reveive data from the server
    file_size = int(receive_data(sock))
    if file_size > 0:
        # downloads file <file name> from the server
        content = sock.recv(file_size)
        with open(file_name, 'wb') as f:
            f.write(content)
        print(f"Downloaded {file_name}")
    else:
        print("File not found")


def ftp_put(sock, file_name):
    try:
        with open(file_name, 'rb') as f:
            content = f.read()
        # send data
        send_data(sock, f"PUT {file_name}")
        send_data(sock, f"{len(content)}")
        # uploads file <file name> to the server
        sock.sendall(content)
        print(receive_data(sock))
    except FileNotFoundError:
        print("File not found")


def ftp_ls(sock):
    # send command to server
    send_data(sock, "LS")
    # lists files on the server
    print(receive_data(sock))


def ftp_quit(sock):
    # disconnects from the server and exits
    send_data(sock, "QUIT")
    sock.close()
    print("Disconnected from server")
    sys.exit()


# Helper functions
def send_data(sock, data):
    sock.sendall(data.encode())

def receive_data(sock):
    return sock.recv(1024).decode()


if __name__ == "__main__":
    # TODO: input validation / error handling wherever needed

    if len(sys.argv) != 3:
        print("Usage: python cli.py <server machine> <server port>")
        sys.exit()

    serverMachine = sys.argv[1]
    serverPort = int(sys.argv[2])
    try:
        controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        controlSocket.connect((serverMachine, serverPort))
        print("Connected to server.")

        # DNS lookup to get IP address
        #ip = socket.gethostbyname(serverMachine)
        #print("get ip")

        # create control channel socket
        # Control channel lasts throughout the ftp
        # session and is used to transfer all commands (ls, get, and put) from client to server
        # and all status/error messages from server to client.
        #controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("create control socket")

        # create data channel socket 
        #dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("create data socket")

        # connect control
        #controlSocket.connect((ip, serverPort))
        #print("connect control socket")

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
            command = input("Enter a command: ")
            if command.startswith("ftp get"):
                _, _, file_name = command.partition(' ')
                ftp_get(controlSocket, file_name)
            elif command.startswith("ftp put"):
                _, _, file_name = command.partition(' ')
                ftp_put(controlSocket, file_name)
            elif command == "ftp ls":
                ftp_ls(controlSocket)
            elif command == "ftp quit":
                send_data(controlSocket, "QUIT")
                break
            else:
                print("Invalid command")
    finally:
        controlSocket.close()
