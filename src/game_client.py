import pygame
from network import Network
import pickle
from button import Button
import time
from parameter_screen import Parameter_screen
from promote_screen import Promote_screen
pygame.font.init()


class Game_Client() :
    def __init__(self, screen, width, height, resolution, player, network, color,color2,music, rotate) :
        self.screen = screen
        self.width = width
        self.height = height
        self.resolution = resolution
        self.color = color
        self.color2 = color2
        self.music = music
        self.running = True
        self.clock = pygame.time.Clock()
        self.network = network
        self.player = player
        self.font = pygame.font.SysFont('chess_online/assets/Walecriture-Regular.ttf', 30)

        self.buttons = [#quitter
                        Button(self.width-80, 20, 60, 60, "x", 50, "comicsans", True, (0,0,0), self.color2, True,(0,0,0)),
                        Button(20, 20, 200, 60, "Parameters", 30, "comicsans", False, (0,0,0), self.color2, True,(0,0,0))]
        self.delay = 0 #delai entre chaque clic

        self.square_size = (self.height//10,self.height//10) #taille une case echiquier en px
        self.selectioned = 0 #boolean si case selectionée
        self.selectioned_square = None
        self.winner = None
        self.colors = ["white","black"]

        #on cree une liste avec les images des pieces dans le bon sens + la bonne taille + bon endroit
        self.pieces_display = []
        for color in self.colors :
            self.rotate = rotate
            #on tourne les pieces pour la couleur opposée
            if color == self.colors[self.player] :
                self.rotate = 0
            for piece in ["pawn","rook","knight","bishop","queen","king"] :
                self.pieces_display.append(pygame.transform.rotate(
                                            pygame.transform.scale(
                                            pygame.image.load("chess_online/assets/pieces_images/{}_{}.png".format(color,piece))
                                            , self.square_size), 
                                            180*self.rotate))
        
        #téléchargement des .png pour les cases :
        self.squares_display = [pygame.transform.scale(pygame.image.load("chess_online/assets/black_square.jpg"),self.square_size), 
                                pygame.transform.scale(pygame.image.load("chess_online/assets/white_square.jpg"),self.square_size),
                                pygame.transform.scale(pygame.image.load("chess_online/assets/selectioned_square.png"),self.square_size),
                                pygame.transform.scale(pygame.image.load("chess_online/assets/legal_move.png"),self.square_size),
                                pygame.transform.scale(pygame.image.load("chess_online/assets/legal_take_move.png"),self.square_size)]
        #coups legaux si piece selectionnée
        self.legal_moves = []

    #gère les clicks du joueur
    def handling_events(self) :
        #vérifie si la partie est bien lancée
        try:
            self.game = self.network.send("get")
        except:
            self.running = False
            print("Couldn't get game")
        
        #vérifie si la souris du client est cliquée et si le clic est sur le plateau affiché
        if pygame.mouse.get_pressed()[0] and self.width//2-4*self.square_size[0] < pygame.mouse.get_pos()[0] < self.width//2+4*self.square_size[0] and self.height//2-4*self.square_size[0] < pygame.mouse.get_pos()[1] < self.height//2+4*self.square_size[0] and self.delay >= 10 and self.game.playing == self.player:
            
            #formules compliquées pour trouver les coordonnées dans l'echiquier du clic de la souris
            self.x = abs((pygame.mouse.get_pos()[0]-self.width//2+self.square_size[0]*4)//self.square_size[0]-7*self.player)
            self.y = abs((pygame.mouse.get_pos()[1]-self.height//2+self.square_size[0]*4)//self.square_size[0] - 7*abs(self.player-1))
            self.selectioned_square = None

            #vérifie si la case sélectionnée contient une pièce et si aucune pièce n'est sélectionnée
            if self.game.board[self.y][self.x] != None and not self.selectioned :
                #si la case sélectionnée est de la bonne couleur
                if self.game.board[self.y][self.x].color == self.colors[self.player] :
                    #sélectionne la case cliquée et l'envoie au serveur
                    self.network.send(str(self.selectioned)+" "+str(self.x)+" "+str(self.y))
                    self.selectioned = 1
                    self.selectioned_square = [self.y,self.x]
            #désélectionne la case sélectionnée
            elif self.selectioned : 
                promoted_to = None
                if self.game.play_piece.type == "pawn" and (self.y == 0 or self.y == 7) and [self.y, self.x] in self.legal_moves:
                    promoted_to = Promote_screen(self.screen, self.width, self.height, self.resolution,self.player, self.color2,  self.pieces_display, self.square_size[0],self.x,self.network).run()
                to_send = str(self.selectioned)+" "+str(self.x)+" "+str(self.y)
                if promoted_to != None:
                    to_send += " "+str(promoted_to)
                self.network.send(to_send)
                self.selectioned = 0

            self.delay = 0
        self.delay+=1

        
        for event in pygame.event.get():
            #vérifie si on quitte le programme
            if event.type == pygame.QUIT or self.buttons[0].click(pygame.mouse.get_pos()):
                self.running = False
                pygame.quit()
            elif self.buttons[1].click(pygame.mouse.get_pos()):
                self.buttons[1].unhighlight()
                self.color,self.color2, self.music, self.rotate = Parameter_screen(self.screen, self.width, self.height, self.resolution, self.color, self.color2, "Game",self.music, self.rotate).run()
                for button in self.buttons:
                    button.update_color(self.color2)
                self.update_rotate()
            #change la couleur si souris passe sur un bouton
            else :
                for button in self.buttons :
                    if button.on_pos(pygame.mouse.get_pos()):
                        if not button.highlighted:
                            button.highlight()
                    else:
                        button.unhighlight()

    #met à jour les cous légaux et le gagnant
    def update(self) :
        #si l'autre joueur deco ou erreur, on quitte
        if not self.game.ready:
            self.running = False
        #verifie si il y a une victoire ou draw
        if self.game.winner != None :
            self.winner = self.game.winner
        #on recupere les coups legaux de la piece selectionnée
        self.legal_moves = self.game.playing_legal_moves

    #affichage
    def display(self) :
        self.screen.fill(self.color)
        for button in self.buttons :
            button.draw(self.screen)
        
        #affichage des cases
        for lign in range(8) :
            for column in range(8) :
                x = self.width//2 - 4*self.square_size[0] - self.square_size[0]*column*(2*self.player-1) + 7*self.square_size[0]*self.player
                y = self.height//2 + 3*self.square_size[0] + self.square_size[0]*lign*(2*self.player-1) - 7*self.square_size[0]*self.player

                #couleur de la case à afficher
                if column%2 != lign%2 :
                    case = 1
                else :
                    case = 0
                #colore la case en orange si elle est sélectionnée
                if self.selectioned_square == [lign,column]:
                    case = 2
                #affiche
                self.screen.blit(self.squares_display[case] , self.squares_display[case].get_rect(x = x,y = y))

                #affiche les coups léguaux si le joueur est en train de jouer et a sélectionné une case
                if self.game.playing == self.player and self.game.selec and self.selectioned and [lign,column] in self.legal_moves :
                    #case vide
                    if self.game.board[lign][column] == None :
                        self.screen.blit(self.squares_display[3] , self.squares_display[3].get_rect(x = x,y = y))
                    #case avec une piece
                    else :
                        self.screen.blit(self.squares_display[4] , self.squares_display[4].get_rect(x = x,y = y))

        #affiche les pièces, à l'envers pour le joueur adverse si self.rotate == 1
        for lign in range(8) :
            for column in range(8) :  
                piece = self.game.board[lign][column]
                if piece != None:
                    x = self.width//2 - 4*self.square_size[0] + self.square_size[0]*column
                    y = self.height//2 - 4*self.square_size[0] + self.square_size[0]*(7-lign)
                    if self.player == 1 :
                        x = self.width//2 + 3*self.square_size[0] - self.square_size[0]*column
                        y = self.height//2 + 3*self.square_size[0] - self.square_size[0]*(7-lign)
                    piece = self.game.board[lign][column]              
                    self.screen.blit(self.pieces_display[piece.color_index*6+piece.type_index] , 
                                     self.pieces_display[piece.color_index*6+piece.type_index].get_rect(x=x,y=y))
                
        #texte
        if not self.winner :
            self.text = self.font.render("Trait aux "+ ("blancs" if not self.game.playing else "noirs"), 1, (0,0,0))
            self.screen.blit(self.text, (self.width - self.text.get_width() - self.width//10, self.height//2 - self.text.get_height()//2)) 
        #si partie finie
        else : 
            if self.winner == "draw" :
                text = "Its a draw!"
            else : text = self.winner+" wins !"
            self.text = self.font.render(text, 1, (0,0,0))
            self.screen.blit(self.text, (self.width - self.text.get_width() - self.width//10, self.height//2 - self.text.get_height()//2)) 
            pygame.display.flip()
            time.sleep(5)
            self.running = False
        pygame.display.flip()

    #boucle principale
    def run(self) :
        while self.running :
            self.clock.tick(self.resolution)
            self.handling_events()
            self.update()
            self.display()

    #gère la rotation des pièces
    def update_rotate(self):
        print(self.player)
        self.pieces_display = []
        rotate= self.rotate
        print(self.rotate)
        for color in self.colors :
            #on tourne les pieces pour la couleur opposée
            if color == self.colors[self.player] :
                rotate = 0
            for piece in ["pawn","rook","knight","bishop","queen","king"] :
                self.pieces_display.append(pygame.transform.rotate(
                                            pygame.transform.scale(
                                            pygame.image.load("chess_online/assets/pieces_images/{}_{}.png".format(color,piece))
                                            , self.square_size), 
                                            180*rotate))
            rotate = self.rotate