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
    KEYDOWN_z = (SDL_KEYDOWN, SDLK_z)
    KEYDOWN_x = (SDL_KEYDOWN, SDLK_x)
    KEY_SKILL_MAP = {
        (SDL_KEYDOWN, SDLK_a),
        (SDL_KEYDOWN, SDLK_s),
        (SDL_KEYDOWN, SDLK_d)
    }
    image = None

    def __init__(self):
        self.pos = get_canvas_width() // 2, get_canvas_height() // 2
        self.image_idle = gfw.image.load('res/char_01.png')
        self.image_attack = gfw.image.load('res/char_01_atk.png')
        self.image_die = gfw.image.load('res/char_01_die.png')
        self.image_skill = gfw.image.load('res/char_01_skill.png')
        self.speed_move = 100 #이동속도
        self.speed_atk = 10 #공격속도
        self.power = 10 #공격력
        self.time = 0
        self.fidx = 0
        self.action = 6
        self.action_atk = 7
        self.combo = 0
        self.dir = 1
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

    def updateAction(self, dx, ddx, dy):
        self.state.updateAction(dx, ddx, dy)

    def handle_event(self, e):
        self.state.handle_event(e)


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

        frame = self.time * 8#(self.player.speed_move * 0.1)
        self.fidx = int(frame) % 8

    def updateDelta(self, ddx, ddy):
        dx, dy = self.player.delta
        dx += ddx
        dy += ddy
        if ddx != 0:
            self.player.updateAction(dx, ddx, dy)
        elif ddy != 0:
            if self.player.dir < 0:
                if dy != 0:
                    self.player.action = 3
                elif ddy != 0:
                    self.player.updateAction(dx, ddx, dy)
                else:
                    self.player.updateAction(dx, ddx, dy)
            elif self.player.dir > 0:
                if dy != 0:
                    self.player.action = 4
                elif ddy != 0:
                    self.player.updateAction(dx, ddx, dy)
                else:
                    self.player.updateAction(dx, ddx, dy)

        self.player.delta = dx, dy

    def updateAction(self, dx, ddx, dy):
        if dx < 0:
            self.player.action = 3
        elif dx > 0:
            self.player.action = 4
        elif ddx > 0:
            if dy != 0:
                self.player.action = 3
            else:
                self.player.action = 5
        elif ddx == 0:
            if self.player.dir < 0:
                self.player.action = 5
            else:
                self.player.action = 6
        else:
            if dy != 0:
                self.player.action = 4
            else:
                self.player.action = 6

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP:
            self.player.updateDelta(*Player.KEY_MAP[pair])
        elif pair == Player.KEYDOWN_x:
            self.player.set_state(AttackState)
        elif pair == Player.KEYDOWN_z:
            self.player.set_state(DashState)
        elif pair in Player.KEY_SKILL_MAP:
            self.player.set_state(SkillState)


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
        frame = self.time * self.player.speed_atk
        move_speed = max(0, 25 - (frame ** 2))

        dx, dy = self.player.delta
        x, y = self.player.pos
        x += self.player.dir * (self.player.speed_move * (0.02 * move_speed)) * gfw.delta_time
        y += dy * (self.player.speed_move * 0.2) * gfw.delta_time

        self.player.pos = x, y

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
            self.player.updateAction(dx, ddx, dy)
        elif ddy != 0:
            if self.player.dir < 0:
                if dy != 0:
                    self.player.action = 3
                elif ddy != 0:
                    self.player.updateAction(dx, ddx, dy)
                else:
                    self.player.updateAction(dx, ddx, dy)
            elif self.player.dir > 0:
                if dy != 0:
                    self.player.action = 4
                elif ddy != 0:
                    self.player.updateAction(dx, ddx, dy)
                else:
                    self.player.updateAction(dx, ddx, dy)
        self.player.delta = dx, dy

    def updateAction(self, dx, ddx, dy):
        if dx < 0:
            self.player.action = 3
        elif dx > 0:
            self.player.action = 4
        elif ddx > 0:
            if dy != 0:
                self.player.action = 3
            else:
                self.player.action = 5
        elif ddx == 0:
            if self.player.dir < 0:
                self.player.action = 5
            else:
                self.player.action = 6
        else:
            if dy != 0:
                self.player.action = 4
            else:
                self.player.action = 6

    def handle_event(self,e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP:
            self.player.updateDelta(*Player.KEY_MAP[pair])
        elif pair == Player.KEYDOWN_x:
            self.comboswitch += 1

class DashState:
    def get(player):
        if not hasattr(DashState, 'singleton'):
            DashState.singleton = DashState()
            DashState.singleton.player = player
        return DashState.singleton

    def __init__(self):
        self.image_idle = gfw.image.load('res/char_01.png')

    def enter(self):
        self.time = 0
        self.fidx = 0

    def exit(self):
        pass

    def draw(self):
        if self.player.dir == -1:
            dash_dir = 1
        else:
            dash_dir = 2

        x = self.fidx * 64
        y = dash_dir * 64
        self.image_idle.clip_draw(x, y, 64, 64, *self.player.pos)

    def update(self):
        self.time += gfw.delta_time
        frame = self.time * 10#(self.player.speed_move * 0.1)

        self.fidx = int(frame) % 8
        dash_speed = max(0, 150 - ((frame - 3) ** 4))

        x, y = self.player.pos
        x += self.player.dir * (self.player.speed_move * round(0.02 * dash_speed)) * gfw.delta_time

        self.player.pos = x, y

        if frame < 9:
            self.fidx = int(frame) % 8
        else:
            self.player.set_state(IdleState)

    def updateDelta(self, ddx, ddy):
        dx, dy = self.player.delta
        dx += ddx
        dy += ddy
        if ddx != 0:
            self.player.updateAction(dx, ddx, dy)
        elif ddy != 0:
            if self.player.dir < 0:
                if dy != 0:
                    self.player.action = 3
                elif ddy != 0:
                    self.player.updateAction(dx, ddx, dy)
                else:
                    self.player.updateAction(dx, ddx, dy)
            elif self.player.dir > 0:
                if dy != 0:
                    self.player.action = 4
                elif ddy != 0:
                    self.player.updateAction(dx, ddx, dy)
                else:
                    self.player.updateAction(dx, ddx, dy)
        self.player.delta = dx, dy

    def updateAction(self, dx, ddx, dy):
        if dx < 0:
            self.player.action = 3
        elif dx > 0:
            self.player.action = 4
        elif ddx > 0:
            if dy != 0:
                self.player.action = 3
            else:
                self.player.action = 5
        elif ddx == 0:
            if self.player.dir < 0:
                self.player.action = 5
            else:
                self.player.action = 6
        else:
            if dy != 0:
                self.player.action = 4
            else:
                self.player.action = 6

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP:
            self.player.updateDelta(*Player.KEY_MAP[pair])

class SkillState:
    @staticmethod
    def get(player):
        if not hasattr(SkillState, 'singleton'):
            SkillState.singleton = SkillState()
            SkillState.singleton.player = player
        return SkillState.singleton

    def __init__(self):
        self.image_attack = gfw.image.load('res/char_01_skill.png')

    def enter(self):
        pass

    def exit(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass

    def updateDelta(self, ddx, ddy):
        dx, dy = self.player.delta
        dx += ddx
        dy += ddy
        if ddx != 0:
            self.player.updateAction(dx, ddx, dy)
        elif ddy != 0:
            if self.player.dir < 0:
                if dy != 0:
                    self.player.action = 3
                elif ddy != 0:
                    self.player.updateAction(dx, ddx, dy)
                else:
                    self.player.updateAction(dx, ddx, dy)
            elif self.player.dir > 0:
                if dy != 0:
                    self.player.action = 4
                elif ddy != 0:
                    self.player.updateAction(dx, ddx, dy)
                else:
                    self.player.updateAction(dx, ddx, dy)

        self.player.delta = dx, dy

    def updateAction(self, dx, ddx, dy):
        if dx < 0:
            self.player.action = 3
        elif dx > 0:
            self.player.action = 4
        elif ddx > 0:
            if dy != 0:
                self.player.action = 3
            else:
                self.player.action = 5
        elif ddx == 0:
            if self.player.dir < 0:
                self.player.action = 5
            else:
                self.player.action = 6
        else:
            if dy != 0:
                self.player.action = 4
            else:
                self.player.action = 6