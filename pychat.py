
import socket


port = 12345

clients = 20

quit = '<$quit$>'

def create_sock(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(address)
    s.listen(clients)
    print("Connecting... ", address)
    return s

class Hall:
    def __init__(self):
        self.rooms = {} 
        self.room_player_map = {} 

    def welcome_new(self, new_player):
        new_player.socket.sendall(b'Welcome to pychat! Enter your name:\n')

    def list_rooms(self, player):
        
        if len(self.rooms) == 0:
            mesg = 'No chatrooms currently. Create your own!\n' \
                + 'Use [<join> room_name] to create a room.\n'
            player.socket.sendall(msg.encode())
        else:
            mesg = 'Listing current rooms...\n'
            for room in self.rooms:
                mesg += room + ": " + str(len(self.rooms[room].players)) + " player(s)\n"
            player.socket.sendall(mesg.encode())
    
    def handle_mesg(self, player, mesg):
        
        help = b'Help:\n'\
            + b'[list] to list all rooms\n'\
            + b'[join room_name] to join/create/switch to a room\n' \
            + b'[-h] for help\n' \
            + b'[quit] to quit\n' \
            + b'Otherwise start typing' \
            + b'\n'

        print(player.name + " says: " + mesg)
        if "name:" in mesg:
            name = mesg.split()[1]
            player.name = name
            print("New connection from:", player.name)
            player.socket.sendall(help)

        elif "join" in msg:
            same_room = False
            if len(mesg.split()) >= 2: 
                room_name = mesg.split()[1]
                if player.name in self.room_player_map:
                    if self.room_player_map[player.name] == room_name:
                        player.socket.sendall(b'You are already in room: ' + room_name.encode())
                        same_room = True
                    else: 
                        old_room = self.room_player_map[player.name]
                        self.rooms[old_room].remove_player(player)
                if not same_room:
                    if not room_name in self.rooms: 
                        new_room = Room(room_name)
                        self.rooms[room_name] = new_room
                    self.rooms[room_name].players.append(player)
                    self.rooms[room_name].welcome_new(player)
                    self.room_player_map[player.name] = room_name
            else:
                player.socket.sendall(help)

        elif "list" in mesg:
            self.list_rooms(player) 

        elif "-h" in mesg:
            player.socket.sendall(help)
        
        elif "quit" in mesg:
            player.socket.sendall(QUIT_STRING.encode())
            self.remove_player(player)

        else:
          
            if player.name in self.room_player_map:
                self.rooms[self.room_player_map[player.name]].broadcast(player, msg.encode())
            else:
                msg = 'You are currently not in any room! \n' \
                    + 'Use [list] to see available rooms! \n' \
                    + 'Use [join room_name] to join a room! \n'
                player.socket.sendall(mesg.encode())
    
    def remove_player(self, player):
        if player.name in self.room_player_map:
            self.rooms[self.room_player_map[player.name]].remove_player(player)
            del self.room_player_map[player.name]
        print("Player: " + player.name + " has left\n")

    
class Room:
    def __init__(self, name):
        self.players = [] 
        self.name = name

    def welcome_new(self, from_player):
        mesg = self.name + " welcomes: " + from_player.name + '\n'
        for player in self.players:
            player.socket.sendall(msg.encode())
    
    def broadcast(self, from_player, mesg):
        mesg = from_player.name.encode() + b":" + msg
        for player in self.players:
            player.socket.sendall(msg)

    def remove_player(self, player):
        self.players.remove(player)
        exit = player.name.encode() + b"has left the room\n"
        self.broadcast(player, exit)

class Player:
    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name

    def fileno(self):
        return self.socket.fileno()