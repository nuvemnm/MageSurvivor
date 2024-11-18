import os
import time
from os.path import join
from os import walk
from config import *
from Bullet import Bullet
from jogador import Jogador
from enemy import Enemy
from sprite import *
from pytmx.util_pygame import load_pygame
from groups import *
from menu import Menu
from random import randint,choice
from itertools import chain
from score import Score

class Jogo:
    def __init__(self):
        #setup
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.zoom_scale = 1.5
        self.camera_surface = pygame.Surface(
            (WINDOW_WIDTH // self.zoom_scale, WINDOW_HEIGHT // self.zoom_scale)
        )
        pygame.display.set_caption('Mage Survivor')
        
        
        self.clock = pygame.time.Clock()
        self.running = False
        self.load_images()
        self.pause = False
        self.boss_spawned = False
        

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

        #player event
        #self.player_event = pygame.event.custom_type()
        #self.death_event = pygame.event.custom_type()
        
        #gun event
        #self.gun_event = pygame.event.custom_type()
        self.bullet_damage = 10 #variavel auxiliar para atualizar o dano da magia
        self.setup()
        if not self.spawn_positions:
            print("Erro: Nenhuma posição de spawn foi carregada!")


    def load_images(self):
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

        self.enemy_frames = {}
        for folder in folders:
            for folder_path,_,file_names in walk(join(subfolder_path, folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names,key = lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path,file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)


    def setup(self):
        """
        init_time = time.time()
        actual_time = time.time()
        elapsed_time = actual_time - init_time
        """
        
        base_path = os.path.dirname(__file__)
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
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        """

        for obj in map.get_layer_by_name('collisions'):
            collision((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'player':
                self.player = Jogador((obj.x,obj.y), self.player_sprites, self.collision_sprites, self.enemy_sprites, self.bullet_sprites)
            else:
                self.spawn_positions.append((obj.x,obj.y))
        
        #scaled_surf = 
        #caled_rect = 

        #self.display_surface.blit(scaled_surf, scaled_rect)

    #def spawnEnemy(self):
    #  self.enemy = Enemy(choice(self.spawn_positions),choice(list(self.enemy_frames.values())),(self.all_sprites,self.enemy_sprites),self.player, self.collision_sprites, self.bullet_sprites)
    
    def player_collision(self):
        if self.enemy_sprites:
            for enemy in self.enemy_sprites:
                player_sprites = pygame.sprite.spritecollide(enemy, self.player_sprites, False, pygame.sprite.collide_mask)
                if player_sprites:
                    for player in player_sprites:
                        player.dinamicLife -= enemy.damage
                        print(player.dinamicLife)
                        if player.dinamicLife <=0:
                            score = Score(self.player)
                            score.write_score()
                            self.running = False
    

    def zoom(self):
        # Limpa a superfície da câmera
        self.camera_surface.fill((0, 0, 0))

        # Define o deslocamento da câmera com base no jogador
        offset_x = self.player.rect.centerx - (WINDOW_WIDTH // (2 * self.zoom_scale))
        offset_y = self.player.rect.centery - (WINDOW_HEIGHT // (2 * self.zoom_scale))

        # Desenha os grupos de sprites ajustando para a câmera
        for sprite in chain(self.all_sprites, self.player_sprites, self.bullet_sprites):
            # Ajusta a posição do sprite para a câmera
            camera_pos = (
                sprite.rect.x - offset_x,
                sprite.rect.y - offset_y,
            )
            self.camera_surface.blit(sprite.image, camera_pos)

        # Escala a superfície da câmera para a tela
        scaled_surface = pygame.transform.scale(
            self.camera_surface, (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()



    def run(self):  
        # Cria o menu e exibe a tela de menu
        init_time = time.time()
        print(init_time)
        menu = Menu(self.screen)
        self.running = False
        
        self.boss = None

        while not self.running:
            if(ENABLE_MENU == True):
                buttons = menu.display_menu()
                result = menu.handle_menu_events(buttons)

                if result == 1:
                    self.running = True

                pygame.display.flip()#Serve para atulizar "limpar" a tela
            else:
                pygame.display.flip()
                self.running = True

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
                        
            
            
            
            #update
            if self.player.level == self.player.actual_level:  
                #aplica zoom na tela
                self.zoom()

                #Desenha todos os sprites
                self.all_sprites.draw(self.player.rect.center)
                self.player_sprites.draw(self.player.rect.center)
                self.bullet_sprites.draw(self.player.rect.center)
          
                self.all_sprites.update(dt)
                self.player_sprites.update(dt)
                self.bullet_sprites.update(dt)

                self.player.leveling()


            else:
                self.aux_timer = self.player.upgrade_menu(self.screen) 
                pygame.display.flip()       
                self.upgrade_timer += dt
            
            if self.upgrade_timer >= 5 or self.aux_timer >= 5:
                self.player.level = self.player.actual_level 
                self.upgrade_timer = 0
                self.aux_timer = 0
            
            #pygame.display.update()
            self.screen.fill('black')
            

            
            
        pygame.quit()
            
        

jogo = Jogo()
jogo.run()