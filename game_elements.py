import pygame
from config import WHITE


class Raquette:
    def __init__(self, x, y, w=100, h=15):
        self.rect = pygame.Rect(x, y, w, h)
    # Méthodes deplacer(), dessiner()...


class Balle:
    def __init__(self, x, y, rayon=10):
        self.rect = pygame.Rect(x - rayon, y - rayon, rayon * 2, rayon * 2)
        self.vx = 5
        self.vy = -5
    # Méthodes deplacer(), dessiner()...
