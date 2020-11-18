from pico2d import *
import gfw

class Player:
    def __init__(self):
        self.pos = get_canvas_width() // 2, get_canvas_height() // 2
        self.image_idle = gfw.image.load('res/char_01.png')
        self.image_attack = gfw.image.load('res/char_01_atk.png')
        self.dx, self.dy = 0, 0
        self.speed_move = 100
        self.time = 0
        self.fidx = 0
        self.action = 6

    def update(self):
        self.time += gfw.delta_time

        x, y = self.pos
        x += self.dx * self.speed_move * gfw.delta_time
        y += self.dy * self.speed_move * gfw.delta_time

        frame = self.time * 15
        self.fidx = int(frame) % 8

        self.pos = x, y

    def draw(self):
        x = self.fidx * 64
        y = self.action * 64
        self.image_idle.clip_draw(x, y, 64, 64, *self.pos)


    def handle_event(self, e):
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_LEFT:
                self.dx -= 1
                self.action = 3
            elif e.key == SDLK_RIGHT:
                self.dx += 1
                self.action = 4
            elif e.key == SDLK_DOWN:
                self.dy -= 1
            elif e.key == SDLK_UP:
                self.dy += 1
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:
                self.dx += 1
                self.action = 5
            elif e.key == SDLK_RIGHT:
                self.dx -= 1
                self.action = 6
            elif e.key == SDLK_DOWN:
                self.dy += 1
            elif e.key == SDLK_UP:
                self.dy -= 1
