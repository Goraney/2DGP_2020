from pico2d import *
import gfw
import gobj
import life_gauge

attack_delay = True

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
    KEYDOWN_c = (SDL_KEYDOWN, SDLK_c)
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
        self.image_skill_1_R = gfw.image.load('res/char_01_skill_1.png')
        self.image_skill_1_L = gfw.image.load('res/char_01_skill_1_L.png')
        self.image_skill_2_1_R = gfw.image.load('res/char_01_skill_2-1.png')
        self.image_skill_2_1_L = gfw.image.load('res/char_01_skill_2-1_L.png')
        self.image_skill_2_2_R = gfw.image.load('res/char_01_skill_2-2.png')
        self.image_skill_2_2_L = gfw.image.load('res/char_01_skill_2-2_L.png')
        self.image_skill_3_R = gfw.image.load('res/char_01_skill_3.png')
        self.image_skill_3_L = gfw.image.load('res/char_01_skill_3_L.png')
        self.skill_num = 0 #스킬번호
        self.stats_0, self.stats_1, self.stats_2, self.stats_3 = 0, 0, 0, 0
        self.max_stats = 100
        self.power = 10 #공격력
        self.speed_atk = 10  # 공격속도
        self.max_life = 50 #최대체력
        self.speed_move = 100  # 이동속도
        self.life = self.max_life
        self.time = 0
        self.fidx = 0
        self.action = 6
        self.action_atk = 7
        self.combo = 0
        self.dir = 1
        self.delta = 0, 0
        self.state = None
        self.set_state(IdleState)
        self.state_num = 0

        global BOUNDARY_LEFT, BOUNDARY_RIGHT, BOUNDARY_DOWN, BOUNDARY_UP
        BOUNDARY_LEFT = 24
        BOUNDARY_DOWN = 28
        BOUNDARY_RIGHT = get_canvas_width() - BOUNDARY_LEFT
        BOUNDARY_UP = get_canvas_height() - BOUNDARY_DOWN

    def set_state(self, clazz):
        if self.state != None:
            self.state.exit()
        self.state = clazz.get(self)
        self.state.enter()

    def draw(self):
        px, py = self.pos
        gy = py - 64 // 2 - 8
        rate = self.life / self.max_life
        life_gauge.draw(px, gy, 64 - 16, rate)

        self.state.draw()

    def update(self):
        self.power = 10 + (self.stats_0 // 5)  # 공격력
        self.speed_atk = 10 + (self.stats_1 // 10)  # 공격속도
        self.max_life = 50 + (self.stats_2 // 2)  # 최대체력
        self.speed_move = 100 + (self.stats_3)  # 이동속도

        if self.stats_0 > self.max_stats:
            self.stats_0 = self.max_stats
        if self.stats_1 > self.max_stats:
            self.stats_1 = self.max_stats
        if self.stats_2 > self.max_stats:
            self.stats_2 = self.max_stats
        if self.stats_3 > self.max_stats:
            self.stats_3 = self.max_stats
        if self.life > self.max_life:
            self.life = self.max_life

        #print("points = ", self.stats_0, self.stats_1, self.stats_2, self.stats_3)
        #print("s_a, s, p, l = ", self.speed_atk, self.speed_move, self.power, self.max_life)
        self.state.update()

    def updateDelta(self, ddx, ddy):
        self.state.updateDelta(ddx, ddy)

    def updateAction(self, dx, ddx, dy):
        self.state.updateAction(dx, ddx, dy)

    def get_bb(self):
        return self.state.get_bb()

    #def hit_timer(self):
        #self.state.hit_timer()

    def decrease_life(self):
        self.state.decrease_life()

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
        self.player.state_num = 0

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
        x = clamp(BOUNDARY_LEFT, x, BOUNDARY_RIGHT)
        y = clamp(BOUNDARY_DOWN, y, BOUNDARY_UP)
        self.player.pos = x, y

        frame = self.time * 8#(self.player.speed_move * 0.1)
        self.fidx = int(frame) % 8

        if self.player.life <= 0:
            self.player.set_state(DieState)

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

    def get_bb(self):
        x, y = self.player.pos
        return x - 32 + 16, y - 32 + 0, x + 32 - 16, y + 32 - 32

    def decrease_life(self):
        if self.player.life > 0:
            self.player.life -= 10
        else:
            self.player.life = 0

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP:
            self.player.updateDelta(*Player.KEY_MAP[pair])
        elif pair == Player.KEYDOWN_x:
            self.player.set_state(AttackState)
        elif pair == Player.KEYDOWN_z:
            if (self.player.stats_3 > 50): # 이동속도 스탯이 50 이상이면
                self.player.set_state(DashState)
        elif pair == Player.KEYDOWN_c:
            self.player.action = 0
        elif pair in Player.KEY_SKILL_MAP:
            if pair == (SDL_KEYDOWN, SDLK_a):
                if (self.player.stats_0 > 50): # 공격력 스탯이 50 이상이면
                    self.player.skill_num = 1
                    self.player.set_state(SkillState)
            elif pair == (SDL_KEYDOWN, SDLK_s):
                if (self.player.stats_1 > 50): # 공격속도 스탯이 50 이상이면
                    self.player.skill_num = 2
                    self.player.set_state(SkillState)
            elif pair == (SDL_KEYDOWN, SDLK_d):
                if (self.player.stats_2 > 50): # 최대체력 스탯이 50 이상이면
                    self.player.skill_num = 3
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
        self.player.state_num = 1

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
        global attack_delay
        self.time += gfw.delta_time
        frame = self.time * self.player.speed_atk
        move_speed = max(0, 25 - (frame ** 2))

        dx, dy = self.player.delta
        x, y = self.player.pos
        x += self.player.dir * (self.player.speed_move * (0.01 * move_speed)) * gfw.delta_time
        y += dy * (self.player.speed_move * 0.2) * gfw.delta_time
        x = clamp(BOUNDARY_LEFT, x, BOUNDARY_RIGHT)
        y = clamp(BOUNDARY_DOWN, y, BOUNDARY_UP)

        self.player.pos = x, y

        if attack_delay == True and self.fidx == 2:
            for e in gfw.world.objects_at(gfw.layer.enemy):
                if gobj.collides_box(self, e):
                    if self.player.action_atk < 4:
                        atk = 3 - self.player.action_atk
                    else:
                        atk = 3 - (self.player.action_atk - 4)
                    e.life -= round(self.player.power * (0.8 + (0.2 * atk)))
                    attack_delay = False

        if frame < 6:
            self.fidx = int(frame)
        else:
            self.player.combo += 1
            attack_delay = True
            if self.comboswitch == 0:
                self.player.set_state(IdleState)
            else:
                self.player.set_state(AttackState)

        if self.player.life <= 0:
            self.player.set_state(DieState)

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

    def get_bb(self):
        x, y = self.player.pos
        if self.player.dir < 0:
            return x - 32 + (-16), y - 32 + 0, x + 32 - 32, y + 32 - 16
        else:
            return x - 32 + 32, y - 32 + 0, x + 32 - (-16), y + 32 - 16

    def decrease_life(self):
        if self.player.life > 0:
            self.player.life -= 10
        else:
            self.player.life = 0

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
        self.player.state_num = 2

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
        x = clamp(BOUNDARY_LEFT, x, BOUNDARY_RIGHT)
        y = clamp(BOUNDARY_DOWN, y, BOUNDARY_UP)

        self.player.pos = x, y

        if frame < 9:
            self.fidx = int(frame) % 8
        else:
            self.player.set_state(IdleState)

        if self.player.life <= 0:
            self.player.set_state(DieState)

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

    def get_bb(self):
        x, y = self.player.pos
        return x - 32 + 16, y - 32 + 8, x + 32 - 16, y + 32 - 26

    def decrease_life(self):
        if self.player.life > 0:
            self.player.life -= 10
        else:
            self.player.life = 0

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
        self.image_skill_1_R = gfw.image.load('res/char_01_skill_1.png')
        self.image_skill_1_L = gfw.image.load('res/char_01_skill_1_L.png')
        self.image_skill_2_1_R = gfw.image.load('res/char_01_skill_2-1.png')
        self.image_skill_2_1_L = gfw.image.load('res/char_01_skill_2-1_L.png')
        self.image_skill_2_2_R = gfw.image.load('res/char_01_skill_2-2.png')
        self.image_skill_2_2_L = gfw.image.load('res/char_01_skill_2-2_L.png')
        self.image_skill_3_R = gfw.image.load('res/char_01_skill_3.png')
        self.image_skill_3_L = gfw.image.load('res/char_01_skill_3_L.png')

    def enter(self):
        self.time = 0
        self.fidx = 0
        self.player.state_num = 3

    def exit(self):
        pass

    def draw(self):
        if self.player.skill_num == 1:
            x = self.fidx * 256
        else:
            x = self.fidx * 288
        y = 0

        if self.player.skill_num == 1:
            if self.player.dir < 0:
                self.image_skill_1_L.clip_draw(x, y, 256, 192, *self.player.pos)
            else:
                self.image_skill_1_R.clip_draw(x, y, 256, 192, *self.player.pos)
        elif self.player.skill_num == 2:
            if self.player.dir < 0:
                if self.fidx < 6:
                    self.image_skill_2_1_L.clip_draw(x, y, 288, 192, *self.player.pos)
                elif self.fidx == 6:
                    self.fidx -= 6
                    self.image_skill_2_2_L.clip_draw(x, y, 288, 192, *self.player.pos)
                else:
                    self.image_skill_2_2_L.clip_draw(x, y, 288, 192, *self.player.pos)
            else:
                if self.fidx < 6:
                    self.image_skill_2_1_R.clip_draw(x, y, 288, 192, *self.player.pos)
                elif self.fidx == 6:
                    self.fidx -= 6
                    self.image_skill_2_2_R.clip_draw(x, y, 288, 192, *self.player.pos)
                else:
                    self.image_skill_2_2_R.clip_draw(x, y, 288, 192, *self.player.pos)
        elif self.player.skill_num == 3:
            if self.player.dir < 0:
                self.image_skill_3_L.clip_draw(x, y, 288, 192, *self.player.pos)
            else:
                self.image_skill_3_R.clip_draw(x, y, 288, 192, *self.player.pos)

    def update(self):
        global attack_delay
        self.time += gfw.delta_time
        frame = self.time * 10
        if self.player.skill_num == 1:
            frame_limit = 30
        elif self.player.skill_num == 2:
            frame_limit = 23
        elif self.player.skill_num == 3:
            frame_limit = 13

        self.skill_hit()

        if frame < frame_limit:
            self.fidx = int(frame)
        else:
            attack_delay = True
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

    def get_bb(self):
        x, y = self.player.pos
        if self.player.skill_num == 1:
            if self.player.dir < 0:
                return x - 155 + 32, y - 81 + 48, x + 155 - 155, y + 81 - 32
            else:
                return x - 155 + 155, y - 81 + 48, x + 155 - 32, y + 81 - 32
        elif self.player.skill_num > 1:
            return x - 155 + 16, y - 81 + 48, x + 155 - 16, y + 81 - 48

    def decrease_life(self):
        pass

    def skill_hit(self):
        global attack_delay
        if attack_delay == True:
            for e in gfw.world.objects_at(gfw.layer.enemy):
                if gobj.collides_box(self, e):
                    if self.player.skill_num == 1:
                        if self.fidx == 20 or self.fidx == 26:
                            e.life -= round((self.player.power * 1.2) + (self.fidx * 0.7))
                            print("스킬1", round((self.player.power * 1.2) + (self.fidx * 0.7)))
                            attack_delay = False
                    elif self.player.skill_num == 2:
                        hit_frame = [10, 12, 14, 16, 19, 20, 22, 25]
                        for i in hit_frame:
                            if self.fidx == i:
                                e.life -= self.player.power * 0.04 + self.fidx * 0.04
                                print("스킬2", self.player.power * 0.04 + self.fidx * 0.04)
                                #attack_delay = False

                    elif self.player.skill_num == 3:
                        if self.fidx == 10:
                            e.life -= round(self.player.power + self.fidx)
                            self.player.life += round(self.player.power * 0.5)
                            print("스킬3-1", round(self.player.power + self.fidx))
                            print("스킬3-2", round(self.player.power * 0.5), " 회복")

                            attack_delay = False
        else:
            for e in gfw.world.objects_at(gfw.layer.enemy):
                if gobj.collides_box(self, e):
                    if self.player.skill_num == 1:
                        if self.fidx == 25:
                            attack_delay = True


    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP:
            self.player.updateDelta(*Player.KEY_MAP[pair])

class DieState:
    def get(player):
        if not hasattr(DieState, 'singleton'):
            DieState.singleton = DieState()
            DieState.singleton.player = player
        return DieState.singleton

    def __init__(self):
        self.image_die = gfw.image.load('res/char_01_die.png')

    def enter(self):
        self.time = 0
        self.fidx = 0
        self.player.state_num = 4

    def exit(self):
        pass

    def draw(self):
        if self.player.dir == -1:
            die_dir = 0
        else:
            die_dir = 1

        x = self.fidx * 64
        y = die_dir * 64
        self.image_die.clip_draw(x, y, 64, 64, *self.player.pos)

    def update(self):
        self.time += gfw.delta_time
        frame = self.time * 8

        x, y = self.player.pos

        self.player.pos = x, y

        if frame < 24:
            self.fidx = int(frame)
        else:
            gfw.world.remove(self.player)

    def get_bb(self):
        x, y = self.player.pos
        return x - 32 + 16, y - 32 + 0, x + 32 - 32, y + 32 - 32

    def handle_event(self, e):
        pass

    def decrease_life(self):
        pass