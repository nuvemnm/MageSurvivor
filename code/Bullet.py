import math
import os
import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, enemy_sprites, damage):
        # Inicializa a bala como pertencente ao grupo bullet_sprites
        super().__init__(groups)
        
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        image_path = os.path.join(base_path, 'images', 'weapons', 'fire.png')
        self.image = pygame.image.load(image_path)
        self.angle = math.degrees(math.atan2(-direction[1], direction[0]))
        self.image = pygame.transform.rotate(self.image, self.angle)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

        self.enemy_sprites = enemy_sprites

        # self.hitbox_rect = self.rect.inflate(-2,-2)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 3000

        self.direction = direction
        self.speed = 400
        self.damage = damage
    
    def move(self, dt):
        self.rect.x += self.direction[0] * self.speed * dt
        self.rect.y += self.direction[1] * self.speed * dt

    def update(self,dt):
        # Movimenta a bala
        self.move(dt)

        self.check_collision(self.enemy_sprites)
        # Remove a bala após seu tempo de vida
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()


    def check_collision(self, enemy_sprites):
        collision_sprites = pygame.sprite.spritecollide(self, enemy_sprites, False, pygame.sprite.collide_mask)

        if collision_sprites:
            for enemy in collision_sprites:
                enemy.take_damage(self.damage)
            self.kill()
