Anthony Cabacungan, antcabacungan@csu.fullerton.edu
Danny Nguyen, dnguyen1535@csu.fullerton.edu
Zhihuang Chen, zhchen@csu.fullerton.edu

Instructions:

First run the server using:
python serv.py <port number>
    ex. python serv.py 1234

Then run the client with the same port number using:
# python cli.py <server machine> <port number>
    ex. python cli.py localhost 1234

Client will then ask for the following commands:

ftp get <file name> : downloads file <file name> from the server
ftp put <file name> : uploads file <file name> to the server
ftp ls              : lists files on the server
ftp quit            : disconnects from the server and exits