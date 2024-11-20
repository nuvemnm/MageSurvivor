import os
import time
from os.path import join
from os import walk
import utils
from config import *
from Bullet import Bullet
from jogador import Jogador
from enemy import Enemy
from sprite import *
from pytmx.util_pygame import load_pygame
from groups import *

from menus.Menu import Menu
from menus.Main_menu import Main_menu
from menus.Upgrade_menu import Upgrade_menu
from menus.Login_menu import Login_menu

from random import randint,choice

class Jogo:
    def __init__(self):
        #setup
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.camera_surface = pygame.Surface((WINDOW_WIDTH // ZOOM_SCALE, WINDOW_HEIGHT // ZOOM_SCALE))

        pygame.display.set_caption('Mage Survivor')

        self.enemy_frames = utils.load_enemy_images()

        
        self.clock = pygame.time.Clock()

        self.running = False
        self.paused = False
        self.pause = False
        self.boss_spawned = False

        self.upgrade_menu_controller = Upgrade_menu(self.screen)
        self.main_menu_controller = Main_menu(self.screen)
        self.login_menu_controller = Login_menu(self.screen)

        self.active_menu = "main_menu"

        #grupo
        self.all_sprites = AllSprites()
        self.player_sprites = PlayerSprite()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = BulletSprites()
        self.enemy_sprites = pygame.sprite.Group()

        #enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 1500)
        

        self.spawn_positions = []
        self.upgrade_timer = 0
        self.aux_timer = 0

        self.bullet_damage = 10 #variavel auxiliar para atualizar o dano da magia
        self.setup()
        if not self.spawn_positions:
            print("Erro: Nenhuma posição de spawn foi carregada!")

    def setup(self):

        base_path = os.path.dirname(__file__)
        map_path = os.path.join(base_path, 'maps',"firstMap.tmx")
        map_path = os.path.abspath(map_path) 
        #map_path = os.path.abspath(join('/home/UFMG.BR/matheusscarv/Downloads/POO-Projeto-de-Jogo/code/maps/firstMap.tmx'))
        map = load_pygame(map_path)
        for x, y, image in map.get_layer_by_name("grass").tiles():
           Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for x, y, image in map.get_layer_by_name("wall").tiles():
            Sprite_test((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        
        # TODO: Objetos no mapa
        """
        for x, y, image in map.get_layer_by_name("SecondFloor").tiles():
           Sprite_test((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for x, y, image in map.get_layer_by_name("Objects").tiles():
            Sprite_test((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for x, y, image in map.get_layer_by_name("Objects2").tiles():
            Sprite_test((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for x, y, image in map.get_layer_by_name("Details").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        """

        for obj in map.get_layer_by_name('collisions'):
            collision((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'player':
                self.player = Jogador((obj.x,obj.y), self.player_sprites, self.collision_sprites, self.enemy_sprites, self.bullet_sprites)
            else:
                self.spawn_positions.append((obj.x,obj.y))    
                
    def run(self):  
        # Cria o menu e exibe a tela de menu
        init_time = time.time()
        self.running = False
        
        self.boss = None

        while not self.running:
            if(ENABLE_MENU == True):
                if(self.active_menu == "main_menu"):
                    self.main_menu_controller.display_menu(self)
                elif(self.active_menu == "login_menu"):
                    self.login_menu_controller.display_menu(self)
                elif(self.active_menu == "register_menu"):
                    self.register_menu_controller.display_menu(self)
                else:
                    print("ERRO, MENU NAO ENCONTRADO")
                    ## Tratar erro de menu nao encontrado
        pygame.display.flip()


        while self.running:
            keys = pygame.key.get_pressed()
            dt = self.clock.tick(60) / 1000
            actual_time = time.time()
            elapsed_time = actual_time - init_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


                if event.type == self.enemy_event:
                    if elapsed_time >= 0:

                        self.enemy = Enemy(choice(self.spawn_positions),self.enemy_frames['bat'],(self.all_sprites,self.enemy_sprites), self.player, self.collision_sprites, self.bullet_sprites, 20, 20)

                    if elapsed_time >= 5:
                        self.enemy = Enemy(choice(self.spawn_positions),self.enemy_frames['wolf'],(self.all_sprites,self.enemy_sprites), self.player, self.collision_sprites, self.bullet_sprites, 20, 40)
                    if elapsed_time >= 10:

                        self.enemy = Enemy(choice(self.spawn_positions),self.enemy_frames['goblin'],(self.all_sprites,self.enemy_sprites), self.player, self.collision_sprites, self.bullet_sprites, 20, 80)


                    if elapsed_time >= 0 and not self.boss_spawned:
                        self.boss = Enemy(choice(self.spawn_positions),self.enemy_frames['boss'],(self.all_sprites,self.enemy_sprites), self.player, self.collision_sprites, self.bullet_sprites, 20, 80)
                        self.boss_spawned = True

            if self.paused == True:
                pass
                # Pause menu

            elif self.player.upgrading == True:
                self.active_menu = "upgrade_menu"
                self.upgrade_menu_controller.display_menu(self)


            elif self.player.alive == False:
                pass
                # self.game_over()

            else:
                #aplica zoom na tela
                utils.zoom(self.player,self.camera_surface,self.screen,self.all_sprites,self.player_sprites,self.bullet_sprites)
                        
                #Desenha todos os sprites
                self.player_sprites.draw(self.player.rect.center)
                self.bullet_sprites.draw(self.player.rect.center)
                self.all_sprites.draw(self.player.rect.center)
                
                self.all_sprites.update(dt)
                self.player_sprites.update(dt)
                self.bullet_sprites.update(dt)

        
            #pygame.display.update()
        self.screen.fill('black')
            

            
            
        pygame.quit()
            
    def exit(self):
        pygame.quit()

jogo = Jogo()
jogo.run()