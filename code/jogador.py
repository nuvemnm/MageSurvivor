import utils

from os.path import join
import os
from sprite import *
from pytmx.util_pygame import load_pygame
from groups import *
from itertools import chain
from enemy import Enemy
from magias.magia import Spell
import time
from config import *
from upgrade_menu import UpgradeMenu

class Jogador(pygame.sprite.Sprite):
    def __init__(self, position, groups, collision_sprites, enemy_sprites, bullet_sprites):
        super().__init__(groups) 
        
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        image_path = os.path.join(base_path, 'images', 'personagem', 'magomenor.png')
        self.image = pygame.image.load(image_path).convert_alpha()

        self.rect = self.image.get_rect(topleft = position)
        self.level = 1
        self.actual_level = 1
        self.experience = 0
        self.score = 0
        self.nickname = None
        self.password = None

        #movimento
        self.direction = pygame.Vector2()
        self.speed = 300
        self.staticLife = 10
        self.dinamicLife = self.staticLife
        self.collision_sprites = collision_sprites
        self.enemy_sprites = enemy_sprites
        self.bullet_sprites = bullet_sprites
        #ajusta tamanho do personagem
        
        self.hitbox = self.rect.inflate(-30, -30)
        self.alive = True
        self.spell = Spell(self,self.bullet_sprites)
        self.can_shoot = True
        

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

        if pygame.mouse.get_pressed()[0]:
            self.shoot()

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
    
    def leveling(self):
        experience_threshold = 10
        while self.experience >= experience_threshold:
            self.actual_level += 1

            self.experience -= experience_threshold
            experience_threshold +=20
            print(self.score)
            """
            print(self.experience)
            print(experience_threshold)
            print(self.actual_level)
            print(self.dinamicLife)
            """

    def upgrade_menu(self, screen):
        running = True
        self.upgrade_timer = 0
        self.menu = UpgradeMenu(screen)

        while running:
            buttons = self.menu.display_menu()
            result = self.menu.handle_menu_events(buttons)
            if result is not None:
                running = False
                
        if result == 0:
            self.staticLife += 20
            self.upgrade_timer = 5
            print("vida aumentada para: " + str(self.staticLife))
        elif result == 1:
            self.spell.damage += 10
            self.upgrade_timer = 5
            print("dano aumentado para: " + str(self.spell.damage))

        return self.upgrade_timer


    def shoot(self):
        if self.can_shoot == True:
            mouse_direction = utils.get_mouse_direction_relative_to_center()
            
            if(mouse_direction.length() > 0):
                mouse_direction = mouse_direction.normalize()
            
            bullet_initial_pos = self.rect.center
            self.spell.shoot(bullet_initial_pos, mouse_direction,self.enemy_sprites)
            
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()


    def update(self, dt):
        self.input()
        self.move(dt)
        # Verifica se 0.3 segundos passaram desde o último disparo
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= 300:  
                self.can_shoot = True  

