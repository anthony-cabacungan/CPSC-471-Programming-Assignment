# File Transfer Protocol (FTP) Project

## Project Description

This Python project implements a simple command-line interface (CLI) for a File Transfer
Protocol (FTP) client. It allows users to connect to an FTP server, download files from
the server, upload files to the server, list files on the server, and disconnect from the server.

## The Team

- Anthony Cabacungan, antcabacungan@csu.fullerton.edu
- Danny Nguyen, dnguyen1535@csu.fullerton.edu
- Zhihuang Chen, zhchen@csu.fullerton.edu

## Instructions

1. To run the FTP server, open the terminal and execute the following command:

   `python serv.py <port number>`

   Replace `<port number>` with the port number on which you want the server to listen for connections.

   ex. `python serv.py 1234`

2. To run the FTP client, open a new terminal and execute the following command:

   `python cli.py <server machine> <port number>`

   Replace `<server machine>` with the IP address or hostname of the FTP server and `<port number>` with the port number on which the FTP server is running.

   ex. `python cli.py localhost 1234`

3. Upon connecting to the server, the client will then ask for the following commands:

   - `ftp get <file name>` : downloads specified file <file name> from the server
   - `ftp put <file name>` : uploads file <file name> to the server
   - `ftp ls` : lists files on the server
   - `ftp quit` : disconnects from the server and exits

## Notes

The FTP client handles control channel and data channel connections separeately. Upon executing one of the commands, the client ccreates an ephermeral port for data transfer.
