import pygame
from network import Network
import pickle
from button import Button
from game_client import Game_Client
pygame.font.init()

#fenêtre qui apparait entre le menu et le début d'une partie: attente d'un autre joueur

class Waiting_Screen() :
    def __init__(self, screen, width, height, resolution, color,color2,music, rotate) :
        self.screen = screen
        self.width = width
        self.height = height
        self.resolution = resolution
        self.color = color
        self.color2 = color2
        self.music = music
        self.rotate = rotate
        self.running = True
        self.clock = pygame.time.Clock()

        #online
        self.network = Network()
        self.player = int(self.network.get_p())
        print("You are player", self.player)

        self.buttons = [#Menu
                        Button(20, 20, 200, 60, "Menu", 50, "comicsans", False, (0,0,0), self.color2, True,(0,0,0)), 
                        #quitter
                        Button(self.width-80, 20, 60, 60, "x", 50, "comicsans", True, (0,0,0), self.color2, True,(0,0,0))]


    def handling_events(self) :
        #obtient a chaque frame l'objet "game"
        try:
            self.game = self.network.send("get")
        except :
            self.running = False
            print("Couldn't get game")

        for event in pygame.event.get():
            #verifie si on quitte 
            if event.type == pygame.QUIT or self.buttons[1].click(pygame.mouse.get_pos()):
                self.running = False
                pygame.quit()

            #bouton menu
            elif self.buttons[0].click(pygame.mouse.get_pos()):    
                self.running = False

            #changement de couleur si passage de souris sur un bouton
            else :
                for button in self.buttons :
                    if button.on_pos(pygame.mouse.get_pos()):
                        if not button.highlighted:
                            button.highlight()
                    else:
                        button.unhighlight()


    def update(self) :
        #si deux joueurs connectés, on lance la partie
        if self.game.connected() :
            Game_Client(self.screen,self.width,self.height,self.resolution,self.player,self.network, self.color, self.color2,self.music, self.rotate).run()
            self.running = False


    def display(self) :
        self.screen.fill(self.color)

        #Affichage "attente de joueur"
        self.font = pygame.font.SysFont('chess_online/assets/Walecriture-Regular.ttf', 60)
        self.text = self.font.render("Waiting for Player...", 1, (0,0,0))
        self.screen.blit(self.text, (self.width//2 - self.text.get_width()//2, self.height//2 - self.text.get_height()//2-50)) 

        #affichage des boutons
        for button in self.buttons :
            button.draw(self.screen)
        pygame.display.flip()


    def run(self) :
        while self.running :
            self.clock.tick(self.resolution)
            self.handling_events()
            self.update()
            self.display()

