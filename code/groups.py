from typing import List
from pygame import Surface
from pygame.rect import Rect
from config import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH/2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT/2)
        
        sprites = [sprite for sprite in self]

        for sprite in sprites:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)

class PlayerSprite(AllSprites):
    def __init__(self):
        super().__init__()
        
class BulletSprites(AllSprites):
    def __init__(self):
        super().__init__()

class EnemySprites(AllSprites):
    def __init__(self):
        super().__init__()