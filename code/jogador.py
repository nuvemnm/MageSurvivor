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
from menus import Upgrade_menu
from data_manager import Login

class Jogador(pygame.sprite.Sprite):
## TODO: 
    # def player_collision(self):
    #     if self.enemy_sprites:
    #         for enemy in self.enemy_sprites:
    #             player_sprites = pygame.sprite.spritecollide(enemy, self.player_sprites, False, pygame.sprite.collide_mask)
    #             if player_sprites:
    #                 for player in player_sprites:
    #                     player.dinamicLife -= enemy.damage
    #                     print(player.dinamicLife)
    #                     if player.dinamicLife <=0:
    #                         self.running = False




    def __init__(self, position, groups, obstacle_sprites, enemy_sprites, bullet_sprites):
        super().__init__(groups) 
        
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        right_image_path = os.path.join(base_path, 'images', 'personagem', 'magomenor-direita.png')
        self.right_image = pygame.image.load(right_image_path).convert_alpha()

        left_image_path = os.path.join(base_path, 'images', 'personagem', 'magomenor.png')
        self.left_image = pygame.image.load(left_image_path).convert_alpha()
        self.image = self.right_image
        self.login = Login()

        self.rect = self.right_image.get_rect(topleft = position)
        self.position = position
        self.level = 1
        self.actual_level = 1
        self.upgrading = False

        #movimento
        self.direction = pygame.Vector2()
        self.speed = 300
        self.staticLife = 10
        self.dinamicLife = self.staticLife
        self.obstacle_sprites = obstacle_sprites
        self.enemy_sprites = enemy_sprites
        self.bullet_sprites = bullet_sprites
        #ajusta tamanho do personagem
        self.hitbox = self.rect.inflate(-30, -30)
        self.alive = True
        self.experience = 0
        self.experience_threshold = 1
        self.score = 0
        self.spell = Spell(self,self.bullet_sprites)
        self.can_shoot = True
    
        self.invulnerable = False
        self.invulnerable_time = 0
        self.invulnerable_duration = 1000  # Tempo de invulnerabilidade em milissegundos 


    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP]or keys[pygame.K_w])
        #normaliza velocidade diagonal
        self.direction = self.direction.normalize() if self.direction else self.direction
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.image = self.right_image
        elif (keys[pygame.K_LEFT]or keys[pygame.K_a]):
            self.image = self.left_image
        if pygame.mouse.get_pressed()[0]:
            self.shoot()

    def move(self, dt):
        # Movimentação horizontal
        self.hitbox.x += self.direction.x * self.speed * dt
        for obstacle in self.obstacle_sprites:
            if self.hitbox.colliderect(obstacle.rect):
                if self.direction.x > 0:  # Movendo-se para a direita
                    self.hitbox.right = obstacle.rect.left
                elif self.direction.x < 0:  # Movendo-se para a esquerda
                    self.hitbox.left = obstacle.rect.right

        # Movimentação vertical
        self.hitbox.y += self.direction.y * self.speed * dt
        for obstacle in self.obstacle_sprites:
            if self.hitbox.colliderect(obstacle.rect):
                if self.direction.y > 0:  # Movendo-se para baixo
                    self.hitbox.bottom = obstacle.rect.top
                elif self.direction.y < 0:  # Movendo-se para cima
                    self.hitbox.top = obstacle.rect.bottom
        self.rect.center = self.hitbox.center

    def take_damage(self,damage):
        
        self.dinamicLife -= damage
        self.invulnerable = True
        self.invulnerable_time = pygame.time.get_ticks()

        if(self.dinamicLife <= 0):
            self.die()

    def die(self):
        self.alive = False 

    def player_collision(self):
        # Colisão com inimigos
        if not self.invulnerable:
            for enemy in self.enemy_sprites:
                if self.hitbox.colliderect(enemy.rect):
                    self.push_enemy_away(enemy)
                    self.take_damage(enemy.damage)
                    print(f"Vida atual: {self.dinamicLife}")

    def leveling(self):
        print("+1")
        if self.experience == self.experience_threshold:
            self.upgrading = True
            print(f"subiu de nível! nível atual: {self.actual_level}")
        else:
            self.experience += 1
            print(f"experiencia atual: {self.experience}/{self.experience_threshold} ")

    def score_up(self, xp_quantity):
        print(self.nickname)
        print(self.score)
        self.score += xp_quantity
        self.login.write_score(self.nickname, self.score)

    def upgrade(self,stat):
        self.actual_level += 1
        self.experience -= self.experience_threshold
        self.experience_threshold +=3

        if(stat == "damage"):
            print("dano aumentado para: " + str(self.spell.damage))
            self.spell.damage += 10
            self.upgrading = False
        if(stat == "life"):
            self.staticLife += 20
            self.dinamicLife += 20
            print("vida aumentado para: " + str(self.staticLife))
            self.upgrading = False

        return
    
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
        self.control_invulnerability()

        self.input()
        self.move(dt)
        self.player_collision()


        # Verifica se 0.3 segundos passaram desde o último disparo
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= 300:  
                self.can_shoot = True  

    def push_enemy_away(self, enemy):
        # Calcula a direção de afastamento
        direction = pygame.Vector2(enemy.rect.center) - pygame.Vector2(self.rect.center)
        if direction.length() > 0:
            direction = direction.normalize()

        push_strength = 30
        enemy.hitbox_rect.x += direction.x * push_strength
        enemy.hitbox_rect.y += direction.y * push_strength
        enemy.rect.center = enemy.hitbox_rect.center

    def control_invulnerability(self):
        # Controle da invulnerabilidade
        if self.invulnerable:
            self.blink_red()
            current_time = pygame.time.get_ticks()
            if current_time - self.invulnerable_time >= self.invulnerable_duration:
                self.invulnerable = False


    def blink_red(self):
        red_image = self.image.copy()

        # Cria uma superfície vermelha do mesmo tamanho com fundo transparente
        red_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        red_surface.fill((255, 0, 0))  # Vermelho sólido

        # Aplica o vermelho apenas nas partes visíveis do sprite
        red_image.blit(red_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Alterna entre o sprite vermelho e o normal
        current_time = pygame.time.get_ticks()
        if (current_time - self.invulnerable_time) // 100 % 2 == 0:
            self.image = red_image
        else:
            self.image = self.right_image



    
