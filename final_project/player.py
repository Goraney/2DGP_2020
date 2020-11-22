from pico2d import *
import gfw

class IdleState:
    @staticmethod
    def get(player):
        if not hasattr(IdleState, 'singleton'):
            IdleState.singleton = IdleState()
            IdleState.singleton.player = player
        return IdleState.singleton

    def __init__(self):
        self.image_idle = gfw.image.load('res/char_01.png')

    def enter(self):
        self.time = 0
        self.fidx = 0

    def exit(self):
        pass

    def draw(self):
        x = self.fidx * 64
        y = self.player.action * 64
        self.image_idle.clip_draw(x, y, 64, 64, *self.player.pos)

    def update(self):
        self.time += gfw.delta_time
        dx, dy = self.player.delta

        if dx != 0:
            if dx < 0:
                self.player.dir = -1
            elif dx > 0:
                self.player.dir = 1

        x, y = self.player.pos
        x += dx * self.player.speed_move * gfw.delta_time
        y += dy * self.player.speed_move * gfw.delta_time

        self.player.pos = x, y

        frame = self.time * 15
        self.fidx = int(frame) % 8

    def updateDelta(self, ddx, ddy):
        dx, dy = self.player.delta
        dx += ddx
        dy += ddy
        if ddx != 0:
            self.player.updateAction(dx, ddx)
        self.player.delta = dx, dy

    def updateAction(self, dx, ddx):
        self.player.action = \
            3 if dx < 0 else \
            4 if dx > 0 else \
            5 if ddx > 0 else 6

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEYDOWN_MAP:
            self.player.updateDelta(*Player.KEYDOWN_MAP[pair])
        elif pair in Player.KEYUP_MAP:
            self.player.updateDelta(*Player.KEYUP_MAP[pair])
        elif pair == Player.KEYDOWN_z:
            self.player.set_state(AttackState)

class AttackState:
    @staticmethod
    def get(player):
        if not hasattr(AttackState, 'singleton'):
            AttackState.singleton = AttackState()
            AttackState.singleton.player = player
        return AttackState.singleton

    def __init__(self):
        self.image_attack = gfw.image.load('res/char_01_atk.png')

    def enter(self):
        self.time = 0
        self.fidx = 0
        self.comboswitch = 0

        if self.player.dir < 0:
            self.player.action_atk = 3
        else:
            self.player.action_atk = 7

        self.player.action_atk -= self.player.combo % 4

    def exit(self):
        pass

    def draw(self):
        x = self.fidx * 128
        y = self.player.action_atk * 128
        self.image_attack.clip_draw(x, y, 128, 128, *self.player.pos)

    def update(self):
        self.time += gfw.delta_time
        frame = self.time * 15

        if frame < 6:
            self.fidx = int(frame)
        else:
            self.player.combo += 1
            if self.comboswitch == 0:
                self.player.set_state(IdleState)
            else:
                self.player.set_state(AttackState)

    def updateDelta(self, ddx, ddy):
        dx, dy = self.player.delta
        dx += ddx
        dy += ddy
        if ddx != 0:
            self.player.updateAction(dx, ddx)
        self.player.delta = dx, dy

    def updateAction(self, dx, ddx):
        self.player.action = \
            3 if dx < 0 else \
            4 if dx > 0 else \
            5 if ddx > 0 else 6

    def handle_event(self,e):
        pair = (e.type, e.key)
        if pair in Player.KEYDOWN_MAP:
            self.player.updateDelta(*Player.KEYDOWN_MAP[pair])
        elif pair in Player.KEYUP_MAP:
            self.player.updateDelta(*Player.KEYUP_MAP[pair])
        elif pair == Player.KEYDOWN_z:
            self.comboswitch += 1


class Player:
    KEYDOWN_MAP = {
        (SDL_KEYDOWN, SDLK_LEFT):   (-1,  0),
        (SDL_KEYDOWN, SDLK_RIGHT):  ( 1,  0),
        (SDL_KEYDOWN, SDLK_DOWN):   ( 0, -1),
        (SDL_KEYDOWN, SDLK_UP):     ( 0,  1),
    }
    KEYUP_MAP = {
        (SDL_KEYUP, SDLK_LEFT):     ( 1,  0),
        (SDL_KEYUP, SDLK_RIGHT):    (-1,  0),
        (SDL_KEYUP, SDLK_DOWN):     ( 0,  1),
        (SDL_KEYUP, SDLK_UP):       ( 0, -1),
    }
    KEYDOWN_z = (SDL_KEYDOWN, SDLK_z)
    KEYDOWN_x = (SDL_KEYDOWN, SDLK_x)
    image = None

    def __init__(self):
        self.pos = get_canvas_width() // 2, get_canvas_height() // 2
        self.image_idle = gfw.image.load('res/char_01.png')
        self.image_attack = gfw.image.load('res/char_01_atk.png')
        self.image_die = gfw.image.load('res/char_01_die.png')
        self.speed_move = 100
        self.time = 0
        self.fidx = 0
        self.action = 6
        self.action_atk = 7
        self.combo = 0
        self.dir = 0
        self.delta = 0, 0
        self.state = None
        self.set_state(IdleState)

    def set_state(self, clazz):
        if self.state != None:
            self.state.exit()
        self.state = clazz.get(self)
        self.state.enter()

    def draw(self):
        self.state.draw()

    def update(self):
        self.state.update()

    def updateDelta(self, ddx, ddy):
        self.state.updateDelta(ddx, ddy)

    def updateAction(self, dx, ddx):
        self.state.updateAction(dx, ddx)

    def handle_event(self, e):
        self.state.handle_event(e)
