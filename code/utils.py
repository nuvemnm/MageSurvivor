from config import *
import pygame

def get_mouse_direction_relative_to_center():
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    center_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    mouse_relative_pos = pygame.Vector2(mouse_pos) - center_pos
    print(f"mouse_pos: {mouse_pos},center_pos: {center_pos}, mouse_relative_pos:{mouse_relative_pos}")


    return mouse_relative_pos
