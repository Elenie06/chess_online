import pygame
from button import Button
from cursor import Cursor

#paramètres: musique, couleur du fond d'écran

class Parameter_screen :
    def __init__(self, screen, width, height, resolution, color,color2, accessed, music, rotate) :
        self.screen = screen
        self.width = width
        self.height = height
        self.resolution = resolution
        self.running = True
        self.color = color
        self.color2 = color2
        self.music = music
        self.rotate = rotate
        self.clock = pygame.time.Clock() #framerate
        self.music = music
        self.musics = 2

        self.delay = 0

        self.buttons = [#quitter
                        Button(self.width-80, 20, 60, 60, "x", 50, "comicsans", True, (0,0,0), self.color2, True,(0,0,0)) ,
                        #menu
                        Button(20, 20, 200, 60, accessed, 50, "comicsans", False, (0,0,0), self.color2, True,(0,0,0)),
                        #musiques
                        Button(2.6*self.width//3, self.height//3.8, 60, 60, "->", 50, "comicsans", True, (0,0,0), self.color2, True,(0,0,0)),
                        Button(2.1*self.width//3, self.height//3.8, 60, 60, "<-", 50, "comicsans", True, (0,0,0), self.color2, True,(0,0,0)),
                        #rotation des pièces
                        Button(self.width-0.15*self.height, self.height//1.15, 60, 60, "x" if rotate else "", 50, "comicsans", True, (0,0,0), self.color2, True,(0,0,0))]
        self.cursors = [Cursor(self.width//15, self.height//3.5, self.width//3, self.height//100, "Red : ", 25, "comicsans", False, (0,0,0), (0,0,0), True, (255,255,255), self.color[0],(0,255)),
                        Cursor(self.width//15, self.height//3.5 + self.height//10, self.width//3, self.height//100, "Green : ", 25, "comicsans", False, (0,0,0), (0,0,0), True, (255,255,255), self.color[1],(0,255)),
                        Cursor(self.width//15, self.height//3.5 + self.height//5, self.width//3, self.height//100, "Blue : ", 25, "comicsans", False, (0,0,0), (0,0,0), True, (255,255,255), self.color[2],(0,255)),
                        Cursor(2*self.width//3, self.height//2.7, self.width//4, self.height//100, "Volume : ", 25, "comicsans", False, (0,0,0), (0,0,0), True, (255,255,255), int(pygame.mixer.music.get_volume()*100),(0,100))]

    #gère les entrèes de l'utilisateur
    def handling_events(self):
        for event in pygame.event.get() :
            cursor_hold = False
            for cursor in self.cursors:
                if cursor.is_clicked:
                    cursor_hold = True
            if not cursor_hold:
            #Verifie si on quitte
                if event.type == pygame.QUIT or self.buttons[0].click(pygame.mouse.get_pos()) :
                    pygame.quit()
                    self.running = False

                #retour au menu
                elif self.buttons[1].click(pygame.mouse.get_pos()):
                    self.running = False
                
                #musique
                elif self.buttons[2].click(pygame.mouse.get_pos()) and self.delay >= 15:
                    self.music += 1
                    pygame.mixer.music.unload()
                    if self.music > self.musics :
                        self.music = 0
                    pygame.mixer.music.load("chess_online/assets/sounds/bg_music_{}.mp3".format(self.music))
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(self.cursors[3].value/100)
                    self.delay = 0
                elif self.buttons[3].click(pygame.mouse.get_pos()) and self.delay >= 15:
                    self.music-=1
                    pygame.mixer.music.unload()
                    if self.music == -1 :
                        self.music = self.musics
                    pygame.mixer.music.load("chess_online/assets/sounds/bg_music_{}.mp3".format(self.music))
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(self.cursors[3].value/100)
                    self.delay = 0
                elif self.buttons[4].click(pygame.mouse.get_pos()) and self.delay >= 15:
                    self.buttons[4].text = "" if self.buttons[4].text == "x" else "x"
                    self.rotate = 0 if self.rotate == 1 else 1
                    self.delay = 0

                #change couleur si passage de souris sur bouton
                else :
                    for button in self.buttons :
                        if button.on_pos(pygame.mouse.get_pos()):
                            if not button.highlighted:
                                button.highlight()
                        else:
                            button.unhighlight()

            #curseurs
            for cursor in self.cursors :
                if pygame.mouse.get_pressed()[0] and not cursor.is_clicked and cursor.on_pos(pygame.mouse.get_pos()):            
                    cursor.hold()
                    for cursor_ in self.cursors:
                        if cursor_.is_clicked and cursor_!=cursor:
                            cursor.unhold()
                elif pygame.mouse.get_pressed()[0] and cursor.is_clicked:
                    cursor.update_pos(pygame.mouse.get_pos())
                    if cursor == self.cursors[0] :
                        self.color[0] = cursor.value
                        self.color2[0] = cursor.value + 25 if cursor.value <=230 else 255
                    elif cursor == self.cursors[1]:
                        self.color[1] = cursor.value
                        self.color2[1] = cursor.value + 25 if cursor.value <=230 else 255
                    elif cursor == self.cursors[2]:
                        self.color[2] = cursor.value
                        self.color2[2] = cursor.value + 25 if cursor.value <=230 else 255
                    elif cursor == self.cursors[3]:
                        pygame.mixer.music.set_volume(cursor.value/100)
                    for button in self.buttons :
                        button.update_color(self.color2)
                elif not pygame.mouse.get_pressed()[0] and cursor.is_clicked :
                    cursor.unhold()
        self.delay+=1
    
    #affiche les éléments à l'écran
    def draw(self) :
        self.screen.fill(self.color)

        #titre
        font = pygame.font.Font('chess_online/assets/Walecriture-Regular.ttf', 100)
        text = font.render("Parameters", 1, (0,0,0))
        self.screen.blit(text, (self.width//2 - text.get_width()//2, text.get_height()//2))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Colors :", 1, (0,0,0))
        self.screen.blit(text, (self.width//15, self.height//4.5-text.get_height()//2))
        text = font.render("Music :", 1, (0,0,0))
        self.screen.blit(text, (2*self.width//3, self.height//4.5-text.get_height()//2))
        text = font.render("Music "+str(self.music), 1, (0,0,0))
        self.screen.blit(text, (2.27*self.width//3, self.height//3.8))
        text = font.render("Rotate opponent's pieces: ", 1, (0,0,0))
        self.screen.blit(text, (self.width-0.25*self.height-text.get_width(), self.height//1.15))
        
        #boutons
        for button in self.buttons :
            button.draw(self.screen)
        for cursor in self.cursors :
            cursor.draw(self.screen)

        pygame.display.update()
    
    #boucle principale de la fenêtre
    def run(self) :
        while self.running :
            self.clock.tick(self.resolution)
            self.handling_events()
            self.draw()
        return self.color,self.color2,self.music, self.rotate