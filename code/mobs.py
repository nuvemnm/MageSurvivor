from enemy import Enemy

class WeakEnemy(Enemy):
    def __init__(self, pos, frames, groups, player, collision_sprites, bullet_sprites):
        super().__init__(pos, frames, groups, player, collision_sprites, bullet_sprites, damage=10, dinamicLife=20,speed=50)

class MidEnemy(Enemy):
    def __init__(self, pos, frames, groups, player, collision_sprites, bullet_sprites):
        super().__init__(pos, frames, groups, player, collision_sprites, bullet_sprites, damage=25, dinamicLife=50,speed=60)

class StrongEnemy(Enemy):
    def __init__(self, pos, frames, groups, player, collision_sprites, bullet_sprites):
        super().__init__(pos, frames, groups, player, collision_sprites, bullet_sprites, damage=50, dinamicLife=100,speed=50)
        
class BossEnemy(Enemy):
    def __init__(self, pos, frames, groups, player, collision_sprites, bullet_sprites):
        super().__init__(pos, frames, groups, player, collision_sprites, bullet_sprites, damage=100, dinamicLife=500,speed=40)
    
