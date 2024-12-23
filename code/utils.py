from itertools import chain
import pygame
import os
from jogador import Jogador
from Enemies.WeakEnemy import WeakEnemy
from Enemies.MidEnemy import MidEnemy
from Enemies.StrongEnemy import StrongEnemy
from Enemies.Boss import Boss
from map import Map
from sprite import Sprite
from config import *
import pygame
from pytmx.util_pygame import load_pygame
import bcrypt
from random import choice

def get_mouse_direction_relative_to_center():
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    center_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    mouse_relative_pos = pygame.Vector2(mouse_pos) - center_pos
    #print(f"mouse_pos: {mouse_pos},center_pos: {center_pos}, mouse_relative_pos:{mouse_relative_pos}")


    return mouse_relative_pos

def encrypt_password(password):
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)




def load_enemy_images():
    # Caminho absoluto para o diretório raiz do projeto
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Constrói o caminho absoluto para os inimigos
    subfolder_path = os.path.join(base_path, 'images','inimigos')

    folders = list(walk(subfolder_path))
    if folders:
        folders = folders[0][1]  # Obtém apenas as subpastas
        print("Pastas encontradas:", folders)

    else:
        folders = []
        print("Nenhuma pasta encontrada dentro de 'images/inimigos'.")

    enemy_frames = {}
    for folder in folders:
        for folder_path,_,file_names in walk(join(subfolder_path, folder)):
            enemy_frames[folder] = []
            for file_name in sorted(file_names,key = lambda name: int(name.split('.')[0])):
                full_path = join(folder_path,file_name)
                surf = pygame.image.load(full_path).convert_alpha()
                enemy_frames[folder].append(surf)
    return enemy_frames

def load_spell_images():
    # Caminho absoluto para o diretório raiz do projeto
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Constrói o caminho absoluto para os inimigos
    subfolder_path = os.path.join(base_path, 'images','magias')

    folders = list(walk(subfolder_path))
    if folders:
        folders = folders[0][1]  # Obtém apenas as subpastas
        print("Pastas encontradas:", folders)

    else:
        folders = []
        print("Nenhuma pasta encontrada dentro de 'images/magias'.")

    spell_frames = {}
    for folder in folders:
        for folder_path,_,file_names in walk(join(subfolder_path, folder)):
            spell_frames[folder] = []
            for file_name in sorted(file_names,key = lambda name: int(name.split('.')[0])):
                full_path = join(folder_path,file_name)
                surf = pygame.image.load(full_path).convert_alpha()
                spell_frames[folder].append(surf)
    return spell_frames

def draw_camera(screen,camera_surface):
    
    # Escala a superfície da câmera para a tela principal
    scaled_surface = pygame.transform.scale(
        camera_surface, (WINDOW_WIDTH, WINDOW_HEIGHT)
    )
    screen.blit(scaled_surface, (0, 0))

def load_map(jogo):
    map_path = os.path.normpath(MAP_PATH)
    jogo.map = Map(map_path)

def setup(jogo):
    load_map(jogo)
    jogo.map.instantiate_grass_sprites(jogo.grass_sprites)
    jogo.map.isntantiate_obstacles_sprites(jogo.obstacle_sprites)
    jogo.player = Jogador(jogo.map.player_spawn_position, jogo.player_sprites, jogo.obstacle_sprites, jogo.enemy_sprites, jogo.bullet_sprites)

def spawn_enemy(jogo, event, timer):
  
    if timer >= 0:
        if event.type == jogo.weak_enemy_event:
            jogo.enemy = WeakEnemy(choice(jogo.map.enemies_spawn_positions),jogo.enemy_frames['bat'],(jogo.all_sprites,jogo.enemy_sprites), jogo.player, jogo.collision_sprites, jogo.bullet_sprites, 20, 20)
            
    if timer >= 120:
        if event.type == jogo.mid_enemy_event:
            jogo.enemy = MidEnemy(choice(jogo.map.enemies_spawn_positions),jogo.enemy_frames['wolf'],(jogo.all_sprites,jogo.enemy_sprites), jogo.player, jogo.collision_sprites, jogo.bullet_sprites, 40, 40)
            pygame.time.set_timer(jogo.weak_enemy_event, 1000)
            
    if timer >= 240:
        if event.type == jogo.strong_enemy_event:
            jogo.enemy = StrongEnemy(choice(jogo.map.enemies_spawn_positions),jogo.enemy_frames['goblin'],(jogo.all_sprites,jogo.enemy_sprites), jogo.player, jogo.collision_sprites, jogo.bullet_sprites, 80, 80)
            pygame.time.set_timer(jogo.weak_enemy_event, 500)
            pygame.time.set_timer(jogo.mid_enemy_event, 1500)

            
    if timer >= 360 and not jogo.boss_spawned:
        jogo.boss = Boss(choice(jogo.map.enemies_spawn_positions),jogo.enemy_frames['boss'],(jogo.all_sprites,jogo.enemy_sprites), jogo.player, jogo.collision_sprites, jogo.bullet_sprites, 300, 1000)
        jogo.boss_spawned = True
        pygame.time.set_timer(jogo.weak_enemy_event, 500)
        pygame.time.set_timer(jogo.mid_enemy_event, 1000)
        pygame.time.set_timer(jogo.strong_enemy_event, 2000) 