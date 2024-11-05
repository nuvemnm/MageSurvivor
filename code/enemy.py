from sprite import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Enemy(pygame.sprite.Sprite): 
    def __init__(self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player
    
        self.frames, self.frames_index =frames,0
        self.image =self.frames[self.frames_index]
        self.animation_speed=6

        self.rect=self.image.get_frect(center=pos)
        self.hitbox_rect=self.rect.inflate(-20,-40)
        self.collision_sprites=collision_sprites
        self.direction =pygame.Vector2()
        self.speed=350