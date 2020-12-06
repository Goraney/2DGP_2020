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
        #if player.state_num == 1:
            #Enemy.decrease_life(e)
        #print("e - ", e.life)
        if e.life <= 0:
            if e.type == 0:
                player.stats_0 += 2
            elif e.type == 1:
                player.stats_1 += 2
            elif e.type == 2:
                player.stats_2 += 2
            elif e.type == 3:
                player.stats_3 += 2
            e.remove()
        #e.remove()
        return

    #if gobj.distance(player.pos, e.pos):
        #print('Player Collision', e)
        #return

    #if e.life <= 0:
        #x, y = e.pos
        #e.remove()

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
                        pass
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

    #print(player.state)
    #print(player.life)

def draw():
    gfw.world.draw()
    gobj.draw_collision_box()

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    if e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()

    player.handle_event(e)

if __name__ == '__main__':
    gfw.run_main()
