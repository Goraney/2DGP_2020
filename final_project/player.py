from pico2d import *
import gfw

class Player:
    KEY_MAP = {
        (SDL_KEYDOWN, SDLK_LEFT):   (-1,  0),
        (SDL_KEYDOWN, SDLK_RIGHT):  ( 1,  0),
        (SDL_KEYDOWN, SDLK_DOWN):   ( 0, -1),
        (SDL_KEYDOWN, SDLK_UP):     ( 0,  1),
        (SDL_KEYUP, SDLK_LEFT):     ( 1,  0),
        (SDL_KEYUP, SDLK_RIGHT):    (-1,  0),
        (SDL_KEYUP, SDLK_DOWN):     ( 0,  1),
        (SDL_KEYUP, SDLK_UP):       ( 0, -1),
    }

    def __init__(self):
        self.pos = get_canvas_width() // 2, get_canvas_height() // 2
        self.image_idle = gfw.image.load('res/char_01.png')
        self.image_attack = gfw.image.load('res/char_01_atk.png')
        self.image_die = gfw.image.load('res/char_01_die.png')
        self.speed_move = 100
        self.time = 0
        self.fidx = 0
        self.action = 6
        self.delta = 0, 0

    def update(self):
        self.time += gfw.delta_time
        dx, dy = self.delta

        x, y = self.pos
        x += dx * self.speed_move * gfw.delta_time
        y += dy * self.speed_move * gfw.delta_time

        self.pos = x, y

        frame = self.time * 15
        self.fidx = int(frame) % 8

    def draw(self):
        x = self.fidx * 64
        y = self.action * 64
        self.image_idle.clip_draw(x, y, 64, 64, *self.pos)

    def updateDelta(self, ddx, ddy):
        dx, dy = self.delta
        dx += ddx
        dy += ddy
        if ddx != 0:
            self.updateAction(dx, ddx)
        self.delta = dx, dy

    def updateAction(self, dx, ddx):
        self.action = \
            3 if dx < 0 else \
            4 if dx > 0 else \
            5 if ddx > 0 else 6

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP:
            self.updateDelta(*Player.KEY_MAP[pair])