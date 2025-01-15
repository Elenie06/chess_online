import pygame
pygame.font.init()

#Bouton: affichage d'un rectangle qui vérifie si il y a un clic dessus

class Button():
    def __init__(self, x, y, width, height, text, text_size, text_font, minuscule, text_color, color, border, border_color, mode = 0) :
        #position
        self.x = x 
        self.y = y
        self.height = height
        self.width = width

        #texte
        self.text = text
        self.minuscule = minuscule
        self.text_color = text_color
        self.text_size = text_size
        self.text_font = text_font
        self.mode = mode

        #affichage
        self.color = color  
        self.original_color = color
        self.border = border
        self.border_color = border_color
        self.border_size = min(self.height//20,self.width//20) 
        self.highlighted = False
        self.selectionned = False

        #couleur si on passe la souris dessus
        self.highlighted_color = 0
        self.update_color(self.color)


    def draw(self, screen) :
        #couleur de fond
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        #affiche la bordure
        if self.border :
            pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.border_size))
            pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.border_size, self.height))
            pygame.draw.rect(screen, self.border_color, (self.x+self.width-self.border_size, self.y, self.border_size, self.height))
            pygame.draw.rect(screen, self.border_color, (self.x, self.y+self.height-self.border_size, self.width, self.border_size))

        #texte bouton
        font = pygame.font.SysFont(self.text_font , self.text_size)
        if self.mode: text = font.render("*"*len(self.text), 1, self.text_color)
        else: text = font.render(self.text , 1 , self.text_color)
        x = self.x - text.get_width()//2 + self.width//2 - 1
        if self.minuscule :
            y = self.y - text.get_height()//1.7 + self.height//2 - 2
        else :
            y = self.y - text.get_height()//2 + self.height//2 - 2
        screen.blit(text, (x, y))

    #vérifient si la position du click est sur le bouton
    def click(self, position) :
        if self.on_pos(position) and pygame.mouse.get_pressed()[0] :
            return True
        return False
    
    def on_pos(self,position) :
        x = position[0]
        y = position[1]
        if self.x <= x <= self.x+self.width and self.y <= y <= self.y+self.height : 
            return True
        return False
    
    #gèrent le changement de couleurs du bouton
    def highlight(self) :
        if not self.highlighted :
            self.highlighted = True
            self.color = self.highlighted_color
        
    def unhighlight(self): 
        if not self.selectionned:
            self.highlighted = False
            self.color = self.original_color

    def update_color(self,color2):
        self.new_color = [255,255,255]
        for color in range(3) :
            self.new_color[color] = color2[color] + 25
            if self.new_color[color] >=255 : 
                self.new_color[color] = 255
        self.highlighted_color = (self.new_color[0],self.new_color[1],self.new_color[2])