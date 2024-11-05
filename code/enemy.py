import os
from os.path import join
from config import *
from jogador import Jogador
from sprite import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Enemy(pygame.sprite.Sprite): 
    def __init__(self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player