import os
import time
from os.path import join
from os import walk
import utils
from config import *
from Bullet import Bullet
from jogador import Jogador
from Enemies.enemy import Enemy
from sprite import *
from groups import *
WHITE = (255, 255, 255)
from menus.Menu import Menu
from menus.Main_menu import Main_menu
from menus.Upgrade_menu import Upgrade_menu
from menus.Register_menu import Register_menu
from menus.Pause_menu import Pause_menu
from menus.Game_over_menu import Game_over

from random import choice

class Jogo:
    def __init__(self):
        #setup
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.camera_surface = pygame.Surface((WINDOW_WIDTH // (2 * ZOOM_SCALE), WINDOW_HEIGHT // (2 * ZOOM_SCALE)))

        pygame.display.set_caption('Mage Survivor')

        self.enemy_frames = utils.load_enemy_images()

        
        self.clock = pygame.time.Clock()

        self.running = False
        self.paused = False
        self.boss_spawned = False
        self.running = True

        self.upgrade_menu_controller = Upgrade_menu(self.screen)
        self.main_menu_controller = Main_menu(self.screen)
        self.register_menu_controller = Register_menu(self.screen)
        self.pause_menu_controller = Pause_menu(self.screen)
        self.gameover_menu_controller = Game_over(self.screen)

        self.text = Menu(self.screen)

        self.active_state = "main_menu"

        #grupo
        self.grass_sprites = SpritesGroup(self.camera_surface)
        self.obstacle_sprites = SpritesGroup(self.camera_surface)

        self.player_sprites = SpritesGroup(self.camera_surface)

        self.bullet_sprites = SpritesGroup(self.camera_surface)

        self.enemy_sprites = SpritesGroup(self.camera_surface)
        self.all_sprites = SpritesGroup(self.camera_surface)
        self.collision_sprites = SpritesGroup(self.camera_surface)

        self.weak_enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.weak_enemy_event, 2000)

        self.mid_enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.mid_enemy_event, 3000)

        self.strong_enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.strong_enemy_event, 4000) 

        self.spawn_positions = []
        self.upgrade_timer = 0
        self.aux_timer = 0

        self.enemy = None

        self.bullet_damage = 10 #variavel auxiliar para atualizar o dano da magia
        if not self.spawn_positions:
            print("Erro: Nenhuma posição de spawn foi carregada!")


    def run(self):  
        # Cria o menu e exibe a tela de menu
        utils.setup(self)

        #self.boss = None

        while self.running:
            if(ENABLE_MENU == True):
                if(self.active_state == "main_menu"):
                    self.main_menu_controller.display_menu(self)
                    self.player.nickname = self.main_menu_controller.user_text
                    self.main_menu_controller.reset(self)
                    self.init_time = time.time()
                
                elif(self.active_state == "register_menu"):
                    self.register_menu_controller.display_menu(self)
                    self.player.nickname = self.register_menu_controller.user_text
                
                elif(self.active_state == "running"):
                    keys = pygame.key.get_pressed()
                    dt = self.clock.tick(60) / 1000
                    self.actual_time = time.time()
                    self.elapsed_time = self.actual_time - self.init_time
                    #print(self.elapsed_time)

                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False


                        utils.spawn_enemy(self, event, self.elapsed_time)
                       


                    if keys[pygame.K_p]:
                        self.pause_menu_controller.pause(self)
                        # Pause menu

                    elif self.player.upgrading == True:
                        self.upgrade_menu_controller.upgrade_choice(self)


                    elif self.player.alive == False:
                        self.active_state = "game_over"
                        # self.game_over()

                    else:
                        #aplica zoom na tela
                        # utils.zoom(self.player,self.screen,[self.all_sprites,self.player_sprites,self.bullet_sprites])

                        self.all_sprites.update(dt)
                        self.grass_sprites.update(dt)
                        self.obstacle_sprites.update(dt)
                        self.player_sprites.update(dt)
                        self.bullet_sprites.update(dt)
                        self.camera_surface.fill((0, 0, 0))  

                        #Desenha todos os sprites
                        self.grass_sprites.draw(self.player.rect.center)
                        self.player_sprites.draw(self.player.rect.center)
                        self.obstacle_sprites.draw(self.player.rect.center)
                        self.bullet_sprites.draw(self.player.rect.center)
                        self.all_sprites.draw(self.player.rect.center)


                        utils.draw_camera(self.screen,self.camera_surface)

                        self.text.display_text(f"Life: {self.player.dinamicLife}", 60, (10,10))
                        self.text.display_text(f"Level: {self.player.actual_level}", 60, (10,50))
                        self.text.display_text(f"Score: {self.player.score}", 60, (10,90))

                    pygame.display.update()

                elif(self.active_state == "game_over"):
                    self.gameover_menu_controller.gameover_options(self)
                    
        self.screen.fill('black')          
        pygame.quit()
            
    def exit(self):
        pygame.quit()

jogo = Jogo()
jogo.run()