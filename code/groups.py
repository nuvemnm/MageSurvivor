from typing import List
from pygame import Surface
from pygame.rect import Rect
from config import *

class SpritesGroup(pygame.sprite.Group):
    def __init__(self,camera_surface):
        super().__init__()
        self.camera_surface = camera_surface
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        self.offset_x = target_pos[0] - (self.camera_surface.get_width()//2)
        self.offset_y = target_pos[1] - (self.camera_surface.get_height()//2)

        sprites = [sprite for sprite in self]

        for sprite in sprites:
            # Calcula o deslocamento de cada sprite
            sprite_rect = sprite.rect.copy()
            
            # Aplica o zoom na posição do sprite
            sprite_rect.x -= self.offset_x
            sprite_rect.y -= self.offset_y 
            
            # Desenha o sprite na câmera, considerando o offset e zoom
            self.camera_surface.blit(sprite.image, sprite_rect.topleft)
