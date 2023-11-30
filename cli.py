# python cli.py <server machine> <server port>

import socket
import sys

# TODO: implement functions
# def ftp_get(file_name):
#     # downloads file <file name> from the server

# def ftp_put(file_name):
#     # uploads file <file name> to the server

# def ftp_ls():
#     # lists files on the server

def ftp_quit(client_socket):
    # disconnects from the server and exits
    clientSocket.close()
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

        # create socket 
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to server
        clientSocket.connect((ip, serverPort))

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

        while True:
            userInput = input("Enter a command: ")
            arguments = userInput.split()
            if arguments[0] == "ftp":
                if arguments[1] == "get":
                    print("get")
                elif arguments[1] == "put":
                    print("put")
                elif arguments[1] == "ls":
                    print("put")
                elif arguments[1] == "quit":
                    ftp_quit(clientSocket)
                    break
            else:
                print("Not a valid command")
                print()
    except:
        print("Cannot connect to server")