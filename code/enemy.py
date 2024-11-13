
from sprite import *
from pytmx.util_pygame import load_pygame
from groups import *
from config import *
from os.path import join
import os
from itertools import chain

class Enemy(pygame.sprite.Sprite): 
    def __init__(self, pos, frames, groups, player, player_sprites, collision_sprites, bullet_sprites, bullet, damage, dinamicLife):
        super().__init__(groups)
        self.player_sprites = player_sprites
        self.player = player
        self.bullet = bullet
    
        self.frames, self.frames_index = frames, 0
        self.image = self.frames[self.frames_index]
        self.animation_speed = 6

        self.rect = self.image.get_rect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20,-40)
        self.collision_sprites = collision_sprites
        self.bullet_sprites = bullet_sprites
        self.direction = pygame.Vector2()
        self.speed = 150
        self.damage = damage
        self.dinamicLife = dinamicLife
        self.alive = True

    def animate(self, dt):
        self.frames_index += self.animation_speed * dt
        self.image = self.frames[(int(self.frames_index) % len(self.frames))]

    def move(self, dt):
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center) 
        self.direction = None
        zero = player_pos == enemy_pos
        if zero:
            #print("0")
            self.direction = 0
        else:
            self.direction = (player_pos - enemy_pos).normalize()
            
            self.hitbox_rect.x += self.direction.x * self.speed *dt
            self.collision('horizontal')
            self.hitbox_rect.y += self.direction.y * self.speed *dt
            self.collision('vertical')
            self.rect.center = self.hitbox_rect.center

        """
        self.hitbox_rect.x += self.direction.x * self.speed *dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed *dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center
        """   

    def collision(self, direction):
        for sprite in chain(self.collision_sprites, self.player_sprites):
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: 
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
        for sprite in self.bullet_sprites: 
            if sprite.rect.colliderect(self.hitbox_rect):
                self.takeDamage()
        

    def takeDamage(self):
        if self.dinamicLife != 0:
            self.dinamicLife = self.dinamicLife - self.bullet.damage
            print(self.dinamicLife)
        else:
            self.kill_self()

    def kill_self(self):
        self.alive = False
        self.kill()

    def update(self, dt):
        self.move(dt)
        self.animate(dt)

"""
class Enemy(pygame.sprite.Sprite): 
    def __init__(self, pos, frames, groups, player, collision_sprites, bullet_sprites):
        super().__init__(groups)
        self.player = player
    
        self.frames, self.frames_index = frames,0
        self.image = self.frames[self.frames_index]
        self.animation_speed = 6

        self.rect=self.image.get_rect(center=pos)
        self.hitbox_rect=self.rect.inflate(-20,-40)
        self.collision_sprites=collision_sprites
        self.bullet_sprites = bullet_sprites
        self.direction = pygame.Vector2()
        self.speed=150
        self.damage = 5

    def animate(self, dt):
        self.frames_index += self.animation_speed * dt
        self.image = self.frames[(int(self.frames_index) % len(self.frames))]

    def move(self, dt):
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center) 
        self.direction = None
        zero = player_pos == enemy_pos
        if zero:
            #print("0")
            self.direction = 0
        else:
            self.direction = (player_pos - enemy_pos).normalize()
            
            self.hitbox_rect.x += self.direction.x * self.speed *dt
            self.collision('horizontal')
            self.hitbox_rect.y += self.direction.y * self.speed *dt
            self.collision('vertical')
            self.rect.center = self.hitbox_rect.center

    
        self.hitbox_rect.x += self.direction.x * self.speed *dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed *dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center
         

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: 
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
        for sprite in self.bullet_sprites: 
            if sprite.rect.colliderect(self.hitbox_rect):
                self.kill()


    def update(self, dt):
        self.move(dt)
        self.animate(dt)

    
"""