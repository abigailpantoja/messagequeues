import select
import socket
import sys

from pychat import Room, Hall, Player
import pychat


server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_connection.connect((sys.argv[1], pychat.port))


print("Connected to server\n")

user= ''

socket_list= [sys.stdin, server_connection]

buff = 4096

while True:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    for s in read_sockets:
        if s is server_connection: 
            mesg= s.recv(buff)
            if not msg:
                print("Server down!")
                sys.exit(2)
            else:
                if mesg == pychat_util.QUIT_STRING.encode():
                    sys.stdout.write('Bye\n')
                    sys.exit(2)
                else:
                    sys.stdout.write(mesg.decode())
                    if 'Please tell us your name' in msg.decode():
                        user = 'name: ' 
                    else:
                        user = ''
                  

        else:
            mesg= user + sys.stdin.readline()
            server_connection.sendall(mesg.encode())