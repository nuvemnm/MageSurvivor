import pygame
from pytmx.util_pygame import load_pygame

import config
from sprite import Sprite


class Map:
    def __init__(self,map_path):
        map = load_pygame(map_path)
        teste = map.get_layer_by_name("grass").tiles()
        print(f"teste: {teste}")
        self.grass = map.get_layer_by_name("grass").tiles()
        self.walls = map.get_layer_by_name("wall").tiles()
        self.enemies_spawn_positions = []
        self.player_spawn_position = pygame.Vector2()

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'player':
                self.player_spawn_position.x = obj.x
                self.player_spawn_position.y = obj.y

            elif obj.name == "enemies":
                self.enemies_spawn_positions.append(pygame.Vector2(obj.x,obj.y))

    def instantiate_grass_sprites(self,grass_group):
        for x,y, image in self.grass:
            Sprite((x * config.TILE_SIZE, y * config.TILE_SIZE), image, grass_group)


    def isntantiate_obstacles_sprites(self,obstacles_group):
        for x,y, image in self.walls:
            Sprite((x * config.TILE_SIZE, y * config.TILE_SIZE), image, obstacles_group)

    def get_player_spawn_pos(self):
        return self.player_spawn_position

    def get_enemies_spawn_pos(self):
        return self.enemies_spawn_positions