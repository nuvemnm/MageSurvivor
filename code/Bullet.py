import os
import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, enemy_sprites, damage):
        # Inicializa a bala como pertencente ao grupo bullet_sprites
        super().__init__(groups)
        
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        image_path = os.path.join(base_path, 'images', 'weapons', 'fire.png')

        self.bullet_surf = pygame.image.load(image_path).convert_alpha()
        self.image = self.bullet_surf
        self.enemy_sprites = enemy_sprites

        
        self.rect = self.image.get_rect(center = pos)
        #self.hitbox_rect = self.rect.inflate(-2,-2)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5000

        self.direction = direction
        self.speed = 100
        self.damage = damage
    
    def update(self):
        print("bullet UPDATE")
        # Movimenta a bala
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        self.check_collision(self.enemy_sprites)
        # Remove a bala após seu tempo de vida
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()


    def check_collision(self, enemy_sprites):
        collision_sprites = pygame.sprite.spritecollide(self, enemy_sprites, False, pygame.sprite.collide_mask)

        if collision_sprites:
            for enemy in collision_sprites:
                enemy.dinamicLife -= self.damage
                #print(enemy.dinamicLife)
                if enemy.dinamicLife <= 0:
                    enemy.destroy()
            self.kill()
