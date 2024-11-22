from sprite import *
from groups import *
from config import *
from os.path import join
import os
from itertools import chain
from Enemies.enemy import Enemy

class MidEnemy(Enemy):
    def __init__(self, pos, frames, groups, player, collision_sprites, bullet_sprites, damage, dinamicLife):
        super().__init__(pos, frames, groups, player, collision_sprites, bullet_sprites, damage, dinamicLife)

        self.speed = 50