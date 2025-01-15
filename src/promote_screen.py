import pygame

#gère la promotion des pièces

class Promote_screen:
    def __init__(self, screen, width, height, resolution,player,color2, pieces_display, square_size,x,network) :
        self.screen = screen
        self.width = width
        self.height = height
        self.resolution = resolution
        self.color2 = color2
        self.player = player
        self.clock = pygame.time.Clock()
        self.pieces_display = pieces_display
        self.running = True
        self.delay = 0
        self.square_size = square_size
        self.x = x
        self.network = network

    #affichage
    def display(self):
        for piece in [1,2,3,4]:
            #affichage
            self.column = self.x if self.player == 0 else abs(self.x-7)
            self.screen.blit(self.pieces_display[self.player*6+piece], self.pieces_display[self.player*6+piece].get_rect(x=(piece-2.5+self.column)*self.square_size+(self.width//2-4*self.square_size),y=0))
        pygame.display.flip()
    
    def update(self):
        for event in pygame.event.get() :
            #Verifie si on quitte
            if event.type == pygame.QUIT :
                pygame.quit()
                self.running = False
        try:
            self.game = self.network.send("get")
        except:
            self.running = False
            print("Couldn't get game")
        if pygame.mouse.get_pressed()[0] and self.delay >= 30 and (self.column-1.5)*self.square_size<=pygame.mouse.get_pos()[0]-self.width//2+4*self.square_size<=(self.column+2.5)*self.square_size and 0<=pygame.mouse.get_pos()[1]<=self.square_size:
            self.selected_piece = int((pygame.mouse.get_pos()[0]-self.width//2+4*self.square_size-(self.column-1.5)*self.square_size)//self.square_size+1)
            print(self.selected_piece)
            self.running = False

    #boucle principale de la fenêtre  
    def run(self):
        while self.running :
            self.clock.tick(self.resolution)
            self.display()
            self.update()
            self.delay+=1
        return self.selected_piece
