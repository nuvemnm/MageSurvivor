import pygame
import os
from Bullet import Bullet


class Spell(pygame.sprite.Sprite):
    def __init__(self,player, bullet_sprites):

        self.bullet_sprites = bullet_sprites
        # self.projectile_image_path
        ## Cooldown padrão:
        self.cooldown = 80
        self.damage = 10
        self.player = player
    
    def shoot(self, bullet_initial_pos, bullet_direction,enemy_sprites):
        bullet = Bullet(pos=bullet_initial_pos,direction=bullet_direction,groups=self.bullet_sprites,enemy_sprites=enemy_sprites,damage=self.damage)
   

    
    


