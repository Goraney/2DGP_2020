from pico2d import *
import gfw
import gobj
import random
from player import *
import life_gauge

die_switch = False

class Enemy:
    SIZE = 64
    def __init__(self):
        self.pos = random.randint(100, 700), random.randint(100, 500)
        self.dx, self.dy = 0, 0
        self.max_life = 100
        self.life = self.max_life
        self.image = gfw.image.load('res/enemy_01.png')

        self.type = random.randint(0, 3)
        self.reset = True
        self.move_speed = 0
        self.fidx = 0
        self.time = 0

    def draw(self):
        x = self.fidx * Enemy.SIZE
        y = self.type * Enemy.SIZE
        self.image.clip_draw(x, y, 64, 64, *self.pos)
        px, py = self.pos
        gy = py - Enemy.SIZE // 2 - 8
        rate = self.life / self.max_life
        life_gauge.draw(px, gy, Enemy.SIZE - 16, rate)

    def update(self):
        self.time += gfw.delta_time
        x, y = self.pos

        self.update_delta()

        x += self.dx * self.move_speed * gfw.delta_time
        y += self.dy * self.move_speed * gfw.delta_time
        self.pos = x, y

        if not self.in_boundary():
            gfw.world.remove(self)

        frame = self.time * 9
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

    def remove(self):
        self.dead()
        gfw.world.remove(self)

    def dead(self):
        e = dead_Enemy(self.pos, self.type)
        gfw.world.add(gfw.layer.dead_enemy, e)

    def get_bb(self):
        half = Enemy.SIZE // 2
        x, y = self.pos
        if self.type == 0:
            return x - half + 16, y - half + 16, x + half - 16, y + half - 16
        elif self.type == 1:
            return x - half + 16, y - half + 4, x + half - 16, y + half - 32
        elif self.type == 2:
            return x - half + 16, y - half + 0, x + half - 16, y + half - 32
        elif self.type == 3:
            return x - half + 12, y - half + 16, x + half - 12, y + half - 16

    def in_boundary(self):
        x,y = self.pos
        if x < -32: return False
        if y < -32: return False
        if x > get_canvas_width() + 32: return False
        if y > get_canvas_height() + 32: return False
        return True

class dead_Enemy:
    def __init__(self, pos, type):
        self.pos = pos
        self.type = type
        self.time = 0
        self.fidx = 0
        self.image_die = gfw.image.load('res/enemy_01_die.png')

    def draw(self):
        x = self.fidx * 64
        y = self.type * 64
        self.image_die.clip_draw(x, y, 64, 64, *self.pos)

    def update(self):
        self.time += gfw.delta_time
        frame = self.time * 8

        x, y = self.pos

        self.pos = x, y

        if frame < 7:
            self.fidx = int(frame)
        else:
            gfw.world.remove(self)

    def get_bb(self):
        half = Enemy.SIZE // 2
        x, y = self.pos
        if self.type == 0:
            return x - half + 16, y - half + 16, x + half - 16, y + half - 16
        elif self.type == 1:
            return x - half + 16, y - half + 4, x + half - 16, y + half - 32
        elif self.type == 2:
            return x - half + 16, y - half + 0, x + half - 16, y + half - 32
        elif self.type == 3:
            return x - half + 12, y - half + 16, x + half - 12, y + half - 16