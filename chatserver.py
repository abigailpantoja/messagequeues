import select
import socket
import sys

from pychat import Hall, Room, Player
import pychat



host = sys.argv[1] if len(sys.argv) >= 2 else ''
listen_sock = pychat.create_sock((host, pychat.port))

hall = Hall()
connection_list = []
connection_list.append(listen_sock)

buff = 4096

while True:
    
    read_players, write_players, error_sockets = select.select(connection_list, [], [])
    for player in read_players:
        if player is listen_sock: 
            new_socket, add = player.accept()
            new_player = Player(new_socket)
            connection_list.append(new_player)
            hall.welcome_new(new_player)

        else: 
            mesg = player.socket.recv(buff)
            if mesg:
                mesg = mesg.decode().lower()
                hall.handle_mesg(player, mesg)
            else:
                player.socket.close()
                connection_list.remove(player)

    for sock in error_sockets: 
        sock.close()
        connection_list.remove(sock)
