from pico2d import *
import gfw
from player import *
import gobj
from enemy import Enemy
import enemy_gen
import threading

canvas_width = 800
canvas_height = 600
gen_timer_switch = True
hit_timer_switch = True
draw_box_switch = False
count = 0

def enter():
    gfw.world.init(['dead_enemy', 'enemy', 'player'])

    global player
    player = Player()
    gfw.world.add(gfw.layer.player, player)

def exit():
    pass

def check_enemy(e):
    if gobj.collides_box(player, e):
        if e.life <= 0:
            if e.type == 0:
                player.stats_0 += 4
            elif e.type == 1:
                player.stats_1 += 4
            elif e.type == 2:
                player.stats_2 += 4
                player.life += 4
            elif e.type == 3:
                player.stats_3 += 4
            e.remove()
        return

def check_player(e):
    global hit_timer_switch
    global count
    if hit_timer_switch == True:
        if gobj.collides_box(player, e):
            if player.state_num == 0 or player.state == 2: # 0:Idle, 2:Dash
                hit_timer_switch = False
                count = 0
                player.decrease_life()
                if player.state_num == 0:
                    if gobj.point_check(player.pos, e.pos):
                        x,y = player.pos
                        x -= (3 - 2 * count) ** 2
                        player.pos = x, y
                    else:
                        x, y = player.pos
                        x += (3 - 2 * count) ** 2
                        player.pos = x, y
                print("hp = ", player.life)
                start_timer()
            elif player.state == 1 or player.state == 3: # 1:Attack, 3:Skill
                pass
            elif player.state == 4: # 4:Die
                pass

def start_timer():
    global hit_timer_switch
    global count
    timer = threading.Timer(0.5, start_timer)
    timer.start()
    count += 0.5
    if count > 1:
        hit_timer_switch = True
        timer.cancel()

def update():
    global gen_timer_switch
    gfw.world.update()
    if gen_timer_switch == True:
        enemy_gen.gen_timer()
        gen_timer_switch = False

    for e in gfw.world.objects_at(gfw.layer.enemy):
        check_enemy(e)
        check_player(e)

def draw():
    global draw_box_switch
    gfw.world.draw()

    if draw_box_switch == True:
        gobj.draw_collision_box()

def handle_event(e):
    global draw_box_switch

    if e.type == SDL_QUIT:
        gfw.quit()
    if e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()
        elif e.key == SDLK_1:
            player.stats_0 += 5
        elif e.key == SDLK_2:
            player.stats_1 += 5
        elif e.key == SDLK_3:
            player.stats_2 += 5
        elif e.key == SDLK_4:
            player.stats_3 += 5
        elif e.key == SDLK_0:
            if draw_box_switch == False:
                draw_box_switch = True
            else:
                draw_box_switch = False

    player.handle_event(e)

if __name__ == '__main__':
    gfw.run_main()
