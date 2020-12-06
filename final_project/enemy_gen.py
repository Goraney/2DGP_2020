import random
import gfw
from pico2d import *
from enemy import Enemy
import threading

MAX_ENEMY_COUNT = 20
COUNT = 0

def generate_enemy():
    e = Enemy()
    gfw.world.add(gfw.layer.enemy, e)

def gen_timer():
    if gfw.world.count_at(gfw.layer.enemy) < MAX_ENEMY_COUNT:
        generate_enemy()
        generate_enemy()
    timer = threading.Timer(3, gen_timer)
    timer.start()