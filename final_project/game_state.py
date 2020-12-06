from pico2d import *
import gfw
from player import Player
import gobj
from enemy import Enemy
import enemy_gen

canvas_width = 800
canvas_height = 600
timer_switch = True

def enter():
    gfw.world.init(['enemy', 'player'])

    global player
    player = Player()
    gfw.world.add(gfw.layer.player, player)

def exit():
    pass

def check_enemy(e):
    if gobj.collides_box(player, e):
        #print('Player Collision', e)
        #e.remove()
        print("collide")
        return

def update():
    global timer_switch
    gfw.world.update()
    #enemy_gen.update()
    if timer_switch == True:
        enemy_gen.gen_timer()
        timer_switch = False

    for e in gfw.world.objects_at(gfw.layer.enemy):
        check_enemy(e)

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
