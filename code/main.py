import os
from os.path import join
from config import *
from jogador import Jogador
from sprite import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from menu import Menu
from random import randint

class Jogo:
    def __init__(self):
        #setup
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Mage Survivor')
        self.clock = pygame.time.Clock()
        self.menu = True
        self.running = False
        self.load_images()

        #grupo
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        self.setup()

        #gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

    def load_images(self):
        # Caminho absoluto para o diretório raiz do projeto
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        # Constrói o caminho absoluto para a imagem
        image_path = os.path.join(base_path, 'images', 'weapons', 'fire.png')

        # Carrega a imagem usando o caminho absoluto
        self.bullet_surf = pygame.image.load(image_path).convert_alpha()
        #self.bullet_surf = pygame.image.load(join('/home/UFMG.BR/matheusscarv/Downloads/POO-Projeto-de-Jogo/images/weapons/fire.png')).convert_alpha()

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def setup(self):
        
        base_path =os.path.dirname(__file__)
        map_path = os.path.join(base_path, 'maps',"firstMap.tmx")
        map_path = os.path.abspath(map_path) 
        #map_path = os.path.abspath(join('/home/UFMG.BR/matheusscarv/Downloads/POO-Projeto-de-Jogo/code/maps/firstMap.tmx'))
        map = load_pygame(map_path)
        for x, y, image in map.get_layer_by_name("grass").tiles():
           Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for x, y, image in map.get_layer_by_name("wall").tiles():
            Sprite_test((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        """
        for x, y, image in map.get_layer_by_name("SecondFloor").tiles():
           Sprite_test((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for x, y, image in map.get_layer_by_name("Objects").tiles():
            Sprite_test((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for x, y, image in map.get_layer_by_name("Objects2").tiles():
            Sprite_test((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for x, y, image in map.get_layer_by_name("Details").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)"""


        for obj in map.get_layer_by_name('collisions'):
            collision((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'player':
                self.player = Jogador((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
                

    def run(self):  
        # Cria o menu e exibe a tela de menu
        menu = Menu(self.screen)
        menu.display_menu_options()  # Exibe o menu até que o jogador pressione Enter

        # Após sair do menu, o jogo começa
        self.running = True

        while self.menu:  # Loop do menu
            self.menu = menu.display_menu_options()  # Exibe o menu até que o jogador pressione Start ou Quit
            if not self.menu:  # Se o menu foi encerrado
                self.running = True
                self.setup()  # Configura o jogo após o menu


        while self.running:
                dt = self.clock.tick(60) / 1000

    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                
                #update
                self.gun_timer()
                self.input()
                self.all_sprites.update(dt)

                #desenha e atualiza o jogo
                self.screen.fill('black')
                self.all_sprites.draw(self.player.rect.center)
                pygame.display.update()
            
            
            
            
        pygame.quit()
            
        


jogo = Jogo()
jogo.run()