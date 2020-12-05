import random
import gfw
from pico2d import *
from enemy import Enemy

MAX_ENEMY_COUNT = 20

def update():
    if gfw.world.count_at(gfw.layer.enemy) < MAX_ENEMY_COUNT:
        generate_enemy()

def generate_enemy():
    e = Enemy()
    gfw.world.add(gfw.layer.enemy, e)
