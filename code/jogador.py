from config import *
from os.path import join
import os
from sprite import *
from pytmx.util_pygame import load_pygame
from groups import *
from itertools import chain
from enemy import Enemy

class Jogador(pygame.sprite.Sprite):
    def __init__(self, position, groups, collision_sprites, enemy_sprites):
        super().__init__(groups) 
        
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        image_path = os.path.join(base_path, 'images', 'personagem', 'magomenor.png')
        self.image = pygame.image.load(image_path).convert_alpha()

        self.rect = self.image.get_rect(topleft = position)

        #movimento
        self.direction = pygame.Vector2()
        self.speed = 300
        self.__staticLife = 10000
        self.dinamicLife = self.__staticLife
        self.collision_sprites = collision_sprites
        self.enemy_sprites = enemy_sprites
        #ajusta tamanho do personagem
        self.hitbox = self.rect.inflate(-30, -30)
        self.alive = True
        self.experience = 0
        #self.upgrade()
        #self.enemy = Enemy()

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP]or keys[pygame.K_w])
        #normaliza velocidade diagonal
        self.direction = self.direction.normalize() if self.direction else self.direction
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            image_path = os.path.join(base_path, 'images', 'personagem', 'magomenor-direita.png')
            self.image = pygame.image.load(image_path).convert_alpha()
        elif (keys[pygame.K_LEFT]or keys[pygame.K_a]):
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            image_path = os.path.join(base_path, 'images', 'personagem', 'magomenor.png')
            self.image = pygame.image.load(image_path).convert_alpha()
    

    def move(self, dt):
        self.hitbox.x += self.direction.x * self.speed * dt 
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.speed * dt 
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0: 
                        self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
                else:
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
        """
        for sprite in self.enemy_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0: 
                        self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
                else:
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
        """
    
    """
    def takeDamage(self):
        for sprite in self.enemy_sprites:
            if sprite.rect.colliderect(self.hitbox):
                self.dinamicLife -= self.enemy.damage
                if self.dinamicLife == 0:
                    self.kill_self()
    
    def upgrade(self):
        self.font = pygame.font.Font(None, 74)
        self.selected_option = -1
        self.options = ["Melhorar Dano", "Melhorar vida"]

        width = self.screen.get_width()
        height = self.screen.get_height()
    """

   

    def update(self, dt):
        self.input()
        self.move(dt)

