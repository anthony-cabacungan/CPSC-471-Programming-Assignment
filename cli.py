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

# def ftp_quit():
#     # disconnects from the server and exits

if __name__ == "__main__":
    # TODO: input validation / error handling wherever needed

    serverMachine = sys.argv[1]
    serverPort = sys.argv[2]

    # DNS lookup to get IP address
    ip = socket.gethostbyname(serverMachine)

    # TODO: connect to server
    
    # TODO: Upon connecting to the server, the client prints out ftp>, which allows the user to execute
    # the following commands.
        # ftp> get <file name> (downloads file <file name> from the server)
        # ftp> put <filename> (uploads file <file name> to the server)
        # ftp> ls(lists files on theserver)
        # ftp> quit (disconnects from the server and exits)