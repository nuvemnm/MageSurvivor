import os
import time
from os.path import join
from os import walk
from config import *
from jogador import Jogador
from enemy import Enemy
from sprite import *
from pytmx.util_pygame import load_pygame
from groups import *
from menu import Menu
from random import randint,choice
from itertools import chain

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
        self.pause = False
        

        #grupo
        self.all_sprites = AllSprites()
        self.player_sprites = PlayerSprite()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

       

        #gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        #enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 700)
        self.spawn_positions = []
        self.upgrade_timer = 0

        #player event
        #self.player_event = pygame.event.custom_type()
        #self.death_event = pygame.event.custom_type()
        
        #gun event
        #self.gun_event = pygame.event.custom_type()

        self.setup()
        if not self.spawn_positions:
            print("Erro: Nenhuma posição de spawn foi carregada!")


    def load_images(self):
        # Caminho absoluto para o diretório raiz do projeto
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        # Constrói o caminho absoluto para a imagem
        image_path = os.path.join(base_path, 'images', 'weapons', 'fire.png')
        # Constrói o caminho absoluto para os inimigos
        subfolder_path = os.path.join(base_path, 'images','inimigos')

        # Carrega a imagem usando o caminho absoluto
        self.bullet_surf = pygame.image.load(image_path).convert_alpha()
        #self.bullet_surf = pygame.image.load(join('/home/UFMG.BR/matheusscarv/Downloads/POO-Projeto-de-Jogo/images/weapons/fire.png')).convert_alpha()

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


    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.player.rect.center + self.gun.player_direction * 20
            self.bullet = Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites), self.enemy_sprites, 10)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

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
                self.player = Jogador((obj.x,obj.y), self.player_sprites, self.collision_sprites, self.enemy_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x,obj.y))


    #def spawnEnemy(self):
    #  self.enemy = Enemy(choice(self.spawn_positions),choice(list(self.enemy_frames.values())),(self.all_sprites,self.enemy_sprites),self.player, self.collision_sprites, self.bullet_sprites)
    
    def bullet_collision(self):
        if self.bullet_sprites: #and self.enemy_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    for enemy in collision_sprites:
                        enemy.dinamicLife -= bullet.damage
                        #print(enemy.dinamicLife)
                        if enemy.dinamicLife <= 0:
                            enemy.destroy()
                    bullet.kill()
    """
    def player_collision(self):
        if self.enemy_sprites:
            for enemy in self.enemy_sprites:
                player_sprites = pygame.sprite.spritecollide(enemy, self.player_sprites, False, pygame.sprite.collide_mask)
                if player_sprites:
                    for player in player_sprites:
                        player.dinamicLife -= enemy.damage
                        print(player.dinamicLife)
                        if player.dinamicLife <=0:
                            self.running = False
    """
    
    
    def run(self):  
        # Cria o menu e exibe a tela de menu
        init_time = time.time()
        menu = Menu(self.screen, ("New game", "Login", "Quit"))
        self.running = False
    
        while not self.running:
            menu.display_menu()
            result = menu.handle_menu_events()

            if result == 1:
                self.running = True

            pygame.display.flip()#Serve para atulizar "limpar" a tela

        while self.running:
            #keys = pygame.key.get_pressed()
            dt = self.clock.tick(60) / 1000
            actual_time = time.time()
            elapsed_time = actual_time - init_time
            timer = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                 
                if event.type == self.enemy_event:
                    if elapsed_time >= 0:
                        self.enemy = Enemy(choice(self.spawn_positions),self.enemy_frames['bat'],(self.all_sprites,self.enemy_sprites), self.player, self.collision_sprites, self.bullet_sprites, self.bullet, 20, 20)
                    if elapsed_time >= 5:
                        self.enemy = Enemy(choice(self.spawn_positions),self.enemy_frames['wolf'],(self.all_sprites,self.enemy_sprites), self.player, self.collision_sprites, self.bullet_sprites, self.bullet, 20, 40)
                    if elapsed_time >= 10:
                        self.enemy = Enemy(choice(self.spawn_positions),self.enemy_frames['goblin'],(self.all_sprites,self.enemy_sprites), self.player, self.collision_sprites, self.bullet_sprites, self.bullet, 20, 80)
                
                if self.player.alive == False:
                    self.running = False
            
            #update
            if self.player.level == self.player.actual_level:
                
                self.player.leveling()
                self.gun_timer()
                self.all_sprites.update(dt)
                self.player_sprites.update(dt)
                self.bullet_collision()
                #self.player_collision()

                #desenha e atualiza o jogo
                self.all_sprites.draw(self.player.rect.center)
                self.player_sprites.draw(self.player.rect.center)
                pygame.display.update()
            else:
                self.player.upgrade_menu(self.screen)
                pygame.display.flip()
                   

           
            self.upgrade_timer += dt
            #print(self.upgrade_timer)
            if self.upgrade_timer >= 10:
                self.player.level = self.player.actual_level 
                self.upgrade_timer = 0
            
            self.input()
            self.screen.fill('black')
            

            
            
        pygame.quit()
            
        

jogo = Jogo()
jogo.run()