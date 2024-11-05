import pygame

#CONFIGURAR A CLASSE MAPA CERTINHO DPS

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
