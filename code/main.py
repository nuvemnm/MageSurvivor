import os
from os.path import join
from os import walk
from config import *
from jogador import *
from sprite import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from menu import Menu
from random import randint,choice

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
        self.spawnEnemy()

        #grupo
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

       

        #gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        #enemy timer
        self.enemy_event=pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_positions=[]

        self.load_images()
        self.setup()
        if not self.spawn_positions:
            print("Erro: Nenhuma posição de spawn foi carregada!")


    def load_images(self):
        # Caminho absoluto para o diretório raiz do projeto
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        # Constrói o caminho absoluto para a imagem
        image_path = os.path.join(base_path, 'images', 'weapons', 'fire.png')
        # Constrói o caminho absoluto para os inimigos
        folder_path = os.path.join(base_path, 'images','inimigos')

        # Carrega a imagem usando o caminho absoluto
        self.bullet_surf = pygame.image.load(image_path).convert_alpha()
        #self.bullet_surf = pygame.image.load(join('/home/UFMG.BR/matheusscarv/Downloads/POO-Projeto-de-Jogo/images/weapons/fire.png')).convert_alpha()

        folders =list(walk(folder_path))
        if folders:
            folders = folders[0][1]  # Obtém apenas as subpastas
            print("Pastas encontradas:", folders)
        else:
            folders = []
            print("Nenhuma pasta encontrada dentro de 'images/inimigos'.")

        self.enemy_frames={}
        for folder in folders:
            for folder_path,_,file_names in walk(join(folder_path, folder)):
                self.enemy_frames[folder]=[]
                for file_name in sorted(file_names,key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path,file_name)
                    surf =pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)


    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites), self.enemy_sprites)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

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
                self.player = Jogador((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.enemy, self.enemy_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x,obj.y))  

        print("Posições de spawn carregadas:", self.spawn_positions)

    def spawnEnemy(self):
       self.enemy = Enemy(choice(self.spawn_positions),choice(list(self.enemy_frames.values())),(self.all_sprites,self.enemy_sprites),self.player, self.collision_sprites, self.bullet_sprites)

    def run(self):  
        # Cria o menu e exibe a tela de menu
        menu = Menu(self.screen)
        self.running = False
    
        while not self.running:
            menu.display_menu()
            result = menu.handle_menu_events()

            if result == 1:
                self.running = True

            pygame.display.flip()#Serve para atulizar "limpar" a tela


        while self.running:
                dt = self.clock.tick(60) / 1000
    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == self.enemy_event:
                        self.spawnEnemy()
                
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