import pygame
from waiting_screen import Waiting_Screen
from button import Button
from parameter_screen import Parameter_screen
pygame.font.init()

class Menu :
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
        self.clock = pygame.time.Clock() #framerate
        self.buttons = [#quitter
                        Button(self.width-80, 20, 60, 60, "x", 50, "comicsans", True, (0,0,0), self.color2, True,(0,0,0)) , 
                        #lancer partie en ligne
                        Button(self.width//3, self.height//3, self.width//3, self.height//10, "Online Game", 50, "comicsans", False, (0,0,0), self.color2, True, (0,0,0)),
                        #paramètres
                        Button(self.width//3, 1.5*self.height//3, self.width//3, self.height//10, "Parameters", 50, "comicsans", False, (0,0,0), self.color2, True, (0,0,0))
                        ]
        #musique
        pygame.mixer.music.load('chess_online/assets/sounds/bg_music_{}.mp3'.format(self.music))
        pygame.mixer.music.play(-1)

    #gère les entrées de l'utilisateur
    def handling_events(self) :
        for event in pygame.event.get() :
            #Verifie si on quitte
            if event.type == pygame.QUIT or self.buttons[0].click(pygame.mouse.get_pos()) :
                pygame.quit()
                self.running = False

            #bouton online game
            elif self.buttons[1].click(pygame.mouse.get_pos()): 
                Waiting_Screen(self.screen,self.width,self.height,self.resolution, self.color,self.color2,self.music, self.rotate).run()
            
            #bouton paramètres
            elif self.buttons[2].click(pygame.mouse.get_pos()):
                self.buttons[2].unhighlight()
                self.color,self.color2,self.music, self.rotate = Parameter_screen(self.screen, self.width, self.height, self.resolution, self.color, self.color2, "Menu",self.music, self.rotate).run()
                for button in self.buttons :
                    button.update_color(self.color2)

            #change couleur si passage de souris sur bouton
            else :
                for button in self.buttons :
                    if button.on_pos(pygame.mouse.get_pos()):
                        if not button.highlighted:
                            button.highlight()
                    else:
                        button.unhighlight()

    #affiochage des éléments à l'écran
    def draw(self) :
        self.screen.fill(self.color)

        #titre
        font = pygame.font.Font('chess_online/assets/Walecriture-Regular.ttf', 100)
        text = font.render("Chess Game", 1, (0,0,0))
        self.screen.blit(text, (self.width//2 - text.get_width()//2, text.get_height()//2))
        
        #boutons
        for button in self.buttons :
            button.draw(self.screen)


        pygame.display.update()

    #boucle principale de la fenêtre
    def run(self) :
        while self.running :
            self.clock.tick(self.resolution)
            self.handling_events()
            self.draw()
        