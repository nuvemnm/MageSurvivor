import pygame
import os
from Bullet import Bullet


class Spell(pygame.sprite.Sprite):
    def __init__(self,player, bullet_sprites):

        self.bullet_sprites = bullet_sprites
        # self.projectile_image_path
        ## Cooldown padrão:
        self.cooldown = 80
        self.damage = 100
        self.player = player
    
    def shoot(self, bullet_initial_pos, bullet_direction,enemy_sprites):
        bullet = Bullet(bullet_initial_pos,bullet_direction,self.bullet_sprites,enemy_sprites,self.damage)
   

    
    


