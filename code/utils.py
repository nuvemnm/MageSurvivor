from itertools import chain
import os
from config import *
import pygame

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

def zoom(player, camera_surface, screen, all_sprites, player_sprites, bullet_sprites):
    # Limpa a superfície da câmera
    camera_surface.fill((0, 0, 0))

    # Define o deslocamento da câmera com base no jogador
    offset_x = player.rect.centerx - (WINDOW_WIDTH // (2 * ZOOM_SCALE))
    offset_y = player.rect.centery - (WINDOW_HEIGHT // (2 * ZOOM_SCALE))

    # Desenha os grupos de sprites ajustando para a câmera
    for sprite in chain(all_sprites, player_sprites, bullet_sprites):
        # Ajusta a posição do sprite para a câmera
        camera_pos = (
            sprite.rect.x - offset_x,
            sprite.rect.y - offset_y,
        )
        camera_surface.blit(sprite.image, camera_pos)

    # Escala a superfície da câmera para a tela
    scaled_surface = pygame.transform.scale(
        camera_surface, (WINDOW_WIDTH, WINDOW_HEIGHT)
    )
    screen.blit(scaled_surface, (0, 0))

    pygame.display.update()
