# python cli.py <server machine> <server port>

import socket
import sys

# TODO: implement functions
def ftp_get(file_name, control_socket, data_socket):
    # downloads file <file name> from the server
    pass

def ftp_put(file_name, control_socket, data_socket):
    # uploads file <file name> to the server
    pass

def ftp_ls(control_socket, data_socket):
    # lists files on the server
    pass

def ftp_quit(controlSocket, dataSocket):
    # disconnects from the server and exits
    controlSocket.close()
    dataSocket.close()
    print("Disconnected from server")
    sys.exit()

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