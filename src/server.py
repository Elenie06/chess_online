import socket
from _thread import *
import pickle
from game import Game
server = "172.18.41.148"
port = 5555

#serveur: gère la connection entre deux joueurs: envoi des états du plateau de jeu 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((server,port))

sock.listen()
print("Waiting for a connexion, Server Started")

games = {}
ids = 0

#fonction qui tourne en arrière-plan du programme
def threaded_client(connexion, player, id):
    global ids
    connexion.send(str.encode(str(player)))

    while True :
        try :
            data = connexion.recv(4096).decode()

            if id in games :
                game = games[id]

                if not data :
                    break
                else :
                    if data != "get" :
                        game.play(data)
                    connexion.sendall(pickle.dumps(game))
            else : 
                break
        except :
            break
    print ("Lost connection")
    
    if games[id].ready == False:
        del games[id]
        print("Closing game",id)
    else :
        games[id].ready = False
    ids -= 1
    connexion.close()


#boucle principale du programme entier lors des parties
while True :
    connexion,address = sock.accept()
    print("Connected to:",address)

    ids+=1
    player = 0
    game_id = (ids - 1)//2
    if ids % 2 == 1 :
        games[game_id] = Game(game_id)
        print ("Creating new game :",game_id)
    else :
        games[game_id].ready = True
        player = 1
        print("Game", game_id, "started")

    start_new_thread(threaded_client , (connexion, player, game_id))