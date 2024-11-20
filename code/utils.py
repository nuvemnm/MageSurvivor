from itertools import chain
import os
from jogador import Jogador
from map import Map
from sprite import Sprite
from config import *
import pygame
from pytmx.util_pygame import load_pygame


def get_mouse_direction_relative_to_center():
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    center_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    mouse_relative_pos = pygame.Vector2(mouse_pos) - center_pos
    #print(f"mouse_pos: {mouse_pos},center_pos: {center_pos}, mouse_relative_pos:{mouse_relative_pos}")


    return mouse_relative_pos

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
    jogo.player = Jogador(jogo.map.player_spawn_position, jogo.player_sprites, jogo.collision_sprites, jogo.enemy_sprites, jogo.bullet_sprites)