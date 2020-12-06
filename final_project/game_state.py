from pico2d import *
import gfw
from player import *
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
        if player.state == AttackState:
            Enemy.decrease_hp(e)
        print('Player Collision', e)
        #e.remove()
        return

    #if gobj.distance(player.pos, e.pos):
        #print('Player Collision', e)
        #return

    #if e.life <= 0:
        #x, y = e.pos
        #e.remove()

def check_player(e):
    if gobj.collides_box(player, e):
        if player.state != SkillState and player.state != DieState:
            player.decrease_life()
            return

def update():
    global timer_switch
    gfw.world.update()
    if timer_switch == True:
        enemy_gen.gen_timer()
        timer_switch = False

    for e in gfw.world.objects_at(gfw.layer.enemy):
        #check_enemy(e)
        check_player(e)



    print(player.life)

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
