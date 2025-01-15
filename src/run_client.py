import pygame
from menu import Menu
import ctypes

# Met en place la taille de la fenêtre et les valeurs par défaut des différents paramètres (musique, couleurs etc.)

pygame.init()
#Taille de la fenetre égale à la taille de l'écran de l'utilisateur
usr32 = ctypes.windll.user32
longueur = usr32.GetSystemMetrics(0)
largeur = usr32.GetSystemMetrics(1)
#Nombre de fps
resolution = 60 
screen = pygame.display.set_mode((longueur, largeur))
menu = Menu(screen, longueur, largeur, resolution, [99,194,111], [124,219,136], 0, 0)
menu.run()
pygame.quit()
