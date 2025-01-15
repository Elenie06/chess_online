import pygame
pygame.font.init()
import math

#bouton rond qui peut être déplacé sur un axe horizontal, et qui peut mesurer sa position sur cet axe

class Cursor():
    def __init__(self, x, y, width, height, text, text_size, text_font, minuscule, text_color, color, border, border_color, value, minmax) :
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

        #affichage
        self.color_rect = color  
        self.color_circle = color
        self.border = border
        self.border_color = border_color
        self.border_size = min(self.height//5,self.width//5) 

        self.is_clicked = False

        self.value = value
        self.minmax = minmax
        self.x_circle = self.x + self.width*(self.value-self.minmax[0])/(self.minmax[1]-self.minmax[0])
        self.y_circle = self.y+self.height//2
        self.radius = self.height*2.5

        #couleur si on passe la souris dessus
        new_color = [255,255,255]
        for color in range(3) :
            new_color[color] = self.color_rect[color]+100
            if new_color[color] >=255 : 
                new_color[color] = 255
        self.highlighted_color = (new_color[0],new_color[1],new_color[2])



    def draw(self, screen) :
        #affiche la bordure + curseur
        if self.border :
            pygame.draw.rect(screen, self.border_color, (self.x-self.border_size, self.y-self.border_size, self.width+2*self.border_size, self.height+2*self.border_size))
        pygame.draw.rect(screen, self.color_rect, (self.x, self.y, self.width, self.height))
        if self.border:
            pygame.draw.circle(screen, self.border_color, (self.x_circle, self.y_circle), self.radius+self.border_size, 0)
        pygame.draw.circle(screen, self.color_circle, (self.x_circle, self.y_circle), self.radius, 0)
        

        #texte au-dessus du curseur
        font = pygame.font.SysFont(self.text_font , self.text_size)
        text = font.render(self.text+str(self.value) , 1 , self.text_color)
        x = self.x - text.get_width()//2 + self.width//2 - 1
        if self.minuscule :
            y = self.y - text.get_height()//1.7 + self.height//2 - 2
        else :
            y = self.y - text.get_height()//2 + self.height//2 - 2
        screen.blit(text, (x, y+self.height*5))

    #vérifient si le click est sur le curseur
    def on_pos(self,position) :
        x = position[0]
        y = position[1]
        if math.sqrt((x-self.x_circle)**2+(y-self.y_circle)**2)<= self.radius: 
            return True
        return False
    
    def update_pos(self,position):
        if self.x<position[0]<self.x+self.width:
            self.x_circle = position[0]
            self.value = (position[0]-self.x)*(self.minmax[1]-self.minmax[0])//self.width+self.minmax[0]
        elif self.x > position[0] :
            self.x_circle = self.x
            self.value = self.minmax[0]
        elif self.x+self.width < position[0] :
            self.x_circle = self.x+self.width
            self.value = self.minmax[1]

    #gèrent le click tenu
    def hold(self) :
        if not self.is_clicked :
            self.is_clicked = True
            self.color_circle = self.highlighted_color
        
    def unhold(self): 
        self.is_clicked = False
        self.color_circle = self.color_rect