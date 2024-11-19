from config import *
import pygame
import bcrypt

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