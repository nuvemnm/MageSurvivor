import pygame
import os
from Bullet import Bullet
import utils


class Spell(pygame.sprite.Sprite):
    def __init__(self,player, bullet_sprites):
        """
        Inicializa a magia com informações básicas, como cooldown e dano.
        """
        self.bullet_sprites = bullet_sprites # Grupo de projéteis
        self.cooldown = 80 # Tempo de espera entre disparos
        self.damage = 5  # Dano causado por cada projétil
        self.player = player
        #self.spell_frames = utils.load_spell_images()
    
    def shoot(self, bullet_initial_pos, bullet_direction,enemy_sprites):
        """
        Dispara um projétil na direção indicada e gerencia sua interação com inimigos.
        """
        # Cria um projétil e o adiciona ao grupo de projéteis
        bullet = Bullet(player=self.player, pos=bullet_initial_pos, direction=bullet_direction,groups=self.bullet_sprites,enemy_sprites=enemy_sprites,damage=self.damage)
        

    
    


