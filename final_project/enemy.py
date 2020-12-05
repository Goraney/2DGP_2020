from pico2d import *
import gfw
import gobj
import random

class Enemy:
    SIZE = 64
    def __init__(self):
        self.pos = self.x, self.y = 200, 200 #수정하자
        self.dx, self.dy = 0, 0
        self.max_life = 100
        self.life = self.max_life
        self.image = gfw.image.load('res/enemy_01.png')
        self.image_die = gfw.image.load('res/enemy_01_die.png')
        self.type = random.randint(0, 3)
        self.reset = True
        self.move_speed = 0
        self.fidx = 0
        self.time = 0

    def draw(self):
        x = self.fidx * Enemy.SIZE
        y = self.type * Enemy.SIZE
        self.image.clip_draw(x, y, 64, 64, *self.pos)

    def update(self):
        self.time += gfw.delta_time
        x, y = self.pos

        self.update_delta()

        x += self.dx * self.move_speed * gfw.delta_time
        y += self.dy * self.move_speed * gfw.delta_time
        self.pos = x, y

        frame = self.time * 7
        self.fidx = int(frame) % 7

    def update_delta(self):
        if self.fidx % 7 == 1:
            if self.reset == True:
                self.dx, self.dy = random.randint(-1, 1), random.randint(-1, 1)
                if self.type == 0:
                    self.move_speed = 1
                elif self.type == 1:
                    self.move_speed = 25
                elif self.type == 2:
                    self.move_speed = 50
                elif self.type == 3:
                    self.move_speed = 150
                self.reset = False
        elif self.fidx % 7 == 4:
            self.reset = True
            self.dx, self.dy = 0, 0

    def get_bb(self):
        half = Enemy.SIZE // 2
        return self.x - half, self.y - half, self.x + half, self.y + half