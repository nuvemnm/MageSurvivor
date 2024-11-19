
from sprite import *
from pytmx.util_pygame import load_pygame
from groups import *
from config import *
from os.path import join
import os
from itertools import chain

class Enemy(pygame.sprite.Sprite): 
    def __init__(self, pos, frames, groups, player, collision_sprites, bullet_sprites, damage, dinamicLife):
        super().__init__(groups)
        #yself.player_sprites = player_sprites
        self.player = player
        #self.bullet = bullet
    
        self.frames, self.frames_index = frames, 0
        self.image = self.frames[self.frames_index]
        self.animation_speed = 6
        
        #rect
        self.rect = self.image.get_rect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20,-40)
        self.collision_sprites = collision_sprites
        self.bullet_sprites = bullet_sprites
        self.direction = pygame.Vector2()
        self.speed = 50

        #life status
        self.damage = damage
        self.dinamicLife = dinamicLife
        self.staticLife = dinamicLife
        self.alive = True

        #timer
        self.death_time = 0
        self.death_duration = 400

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
        
    def take_damage(self,damage):
        if self.alive == False:
            return
        self.dinamicLife -= damage
        if self.dinamicLife <= 0:
            self.destroy()

    def destroy(self):
        self.death_time = pygame.time.get_ticks()
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey('black')
        surf.fill((255, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)
        self.image = surf
        self.alive = False
        
        self.player.leveling(self.staticLife / 5)
        self.player.score_up(self.staticLife)


    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()
            return True

    def update(self, dt):
        if self.death_time == 0:
            self.move(dt)
            self.animate(dt)
        else:
            self.death_timer()

