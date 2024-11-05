import os
from os.path import join
from config import *
from math import atan2, degrees
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from enemy import Enemy

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.ground = True

class Sprite_test(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class collision(pygame.sprite.Sprite):
    def __init__(self, position, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = position)

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        # player conection
        self.player = player
        self.distance = 60
        self.player_direction = pygame.Vector2(0,1)

        # sprite setup
        super(). __init__(groups)
        # Caminho absoluto para o diretório raiz do projeto
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        # Constrói o caminho absoluto para a imagem
        image_path = os.path.join(base_path, 'images', 'weapons', 'spot.png')

        # Carrega a imagem usando o caminho absoluto
        self.gun_surf = pygame.image.load(image_path).convert_alpha()
        #self.gun_surf = pygame.image.load(join('/home/UFMG.BR/matheusscarv/Downloads/POO-Projeto-de-Jogo/images/weapons/spot.png'))
        self.image = self.gun_surf
        self.rect = self.image.get_rect(center = self.player.rect.center + self.player_direction * self.distance)

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = (mouse_pos - player_pos).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)  

    def update(self, _):
        self.get_direction()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        #self.player = player
        #self.bullet_surf = pygame.image.load(join('/home/UFMG.BR/matheusscarv/Downloads/POO-Projeto-de-Jogo/images/weapons/fire.png')).convert_alpha()
        self.image = surf
        self.rect = self.image.get_rect(center = pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5000

        self.direction = direction
        self.speed = 100
        
    def rotate_magic(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x  > 0:
            self.image = pygame.transform.rotozoom(self.bullet_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.bullet_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()

class Enemy(pygame.sprite.Sprite): #depois de testar tem q tirar a classe daqui
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

"""

CRIEI UM ARQUIVO PRA CLASSE MAP FAVOR UTILIZAR SE POSSIVEL RS 
class Map(): 
    def __init__(self, level):
        self.level = level
    
    def loadLevel(level):
        match level:
            case 1:
                map_path = os.path.abspath(join('/home/UFMG.BR/matheusscarv/Downloads/POO-Projeto-de-Jogo/code/maps/firstMap.tmx'))
                map = load_pygame(map_path)
                for x, y, image in map.get_layer_by_name("grass").tiles():
                    Sprite((x * TILE_SIZE, y * TILE_SIZE), image, AllSprites())
                for x, y, image in map.get_layer_by_name("wall").tiles():
                    Sprite_test((x * TILE_SIZE, y * TILE_SIZE), image, AllSprites())
            case 2:
                map_path = os.path.abspath(join('/home/UFMG.BR/matheusscarv/Downloads/POO-Projeto-de-Jogo/code/maps/firstMap.tmx'))
                map = load_pygame(map_path)
                for x, y, image in map.get_layer_by_name("grass").tiles():
                    Sprite((x * TILE_SIZE, y * TILE_SIZE), image, AllSprites())
                for x, y, image in map.get_layer_by_name("wall").tiles():
                    Sprite_test((x * TILE_SIZE, y * TILE_SIZE), image, AllSprites())
"""
