from config import *
from os.path import join
import os
from sprite import *
from pytmx.util_pygame import load_pygame
from groups import *
from itertools import chain
from enemy import Enemy
import time
from config import *

class Jogador(pygame.sprite.Sprite):
    def __init__(self, position, groups, collision_sprites, enemy_sprites):
        super().__init__(groups) 
        
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        image_path = os.path.join(base_path, 'images', 'personagem', 'magomenor.png')
        self.image = pygame.image.load(image_path).convert_alpha()

        self.rect = self.image.get_rect(topleft = position)
        self.level = 1
        self.actual_level = 1
        #movimento
        self.direction = pygame.Vector2()
        self.speed = 300
        self.__staticLife = 10
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
    
    def leveling(self):
        experience_threshold = 10
        while self.experience >= experience_threshold:
            self.actual_level += 1
            self.__staticLife += 20

            self.experience -= experience_threshold
            experience_threshold +=20
            print(self.experience)
            print(experience_threshold)
            print(self.actual_level)
            print(self.dinamicLife)

    def upgrade_menu(self, screen):
        print("alguma coisa")
        font = pygame.font.Font(None, 74)
        # Dimensões e posição da aba
        menu_width, menu_height = 300, 200
        menu_x = (screen.get_width() - menu_width) // 2
        menu_y = (screen.get_height() - menu_height) // 2

        # Janela de upgrade (no centro)
        pygame.draw.rect(screen, (50, 50, 50), (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(screen, (255, 255, 255), (menu_x, menu_y, menu_width, menu_height), 3)

        # Título da aba
        title_text = font.render("Escolha um Upgrade", True, (255, 255, 255))
        screen.blit(title_text, (menu_x + 20, menu_y + 20))
    """
    def upgrade(self):
        #tempo limite para upar
        
        actual_time = time.time()
        limit_time = actual_time - init_time
        
        

        
        
        while limit_time <= 5:
                return True
            else:
                return False

    """

    def update(self, dt):
        self.input()
        self.move(dt)

