import pygame
from magias.magia import Spell

class FireBall(Spell, pygame.sprite.Sprite):

    def __init__(self, player, groups):
        Spell.__init__(self)