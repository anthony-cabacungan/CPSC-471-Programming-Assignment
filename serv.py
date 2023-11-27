# python serv.py <PORTNUMBER>

import socket
import sys

# TODO: input validation / error handling wherever needed

serverPort = sys.argv[1]

if serverPort:
    # TODO: setup server
    print(serverPort)