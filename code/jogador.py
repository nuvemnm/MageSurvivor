from config import *
from os.path import join

class Jogador(pygame.sprite.Sprite):
    def __init__(self, position: int, groups, collision_sprites):
        super().__init__(groups) 
        self.image = pygame.image.load('/home/UFMG.BR/matheusscarv/Downloads/POO-Projeto-de-Jogo/images/personagem/magomenor.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)

        #movimento
        self.direction = pygame.Vector2()
        self.speed = 300
        self.collision_sprites = collision_sprites
        #ajusta tamanho do personagem
        self.hitbox = self.rect.inflate(-15, -30)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP]or keys[pygame.K_w])
        #normaliza velocidade diagonal
        self.direction = self.direction.normalize() if self.direction else self.direction
        if keys[pygame.K_RIGHT]:
            self.image = pygame.image.load('/home/UFMG.BR/matheusscarv/Downloads/POO-Projeto-de-Jogo/images/personagem/magomenor-direita.png').convert_alpha()
        elif keys[pygame.K_LEFT]:
            self.image = pygame.image.load('/home/UFMG.BR/matheusscarv/Downloads/POO-Projeto-de-Jogo/images/personagem/magomenor.png').convert_alpha()

    def move(self, dt):
        self.hitbox.x += self.direction.x * self.speed * dt 
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.speed * dt 
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0: 
                        self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
                else:
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top

    def update(self, dt):
        self.input()
        self.move(dt)