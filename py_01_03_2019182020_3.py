from pico2d import *
import os

## os.chdir('C:\\Users\\HANSUNG\\Desktop\\과제\\2-2\\2DGP\\python_git')

def handle_events():
    global running
    ## global x     ## LEC06
    global dir
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        ## elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            ## running = False      ## LEC06
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                ## x = x + 10 ## LEC06
                dir += 1
            elif event.key == SDLK_LEFT:
                ## x = x - 10 ## LEC06
                dir -= 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
            elif event.key == SDLK_LEFT:
                dir += 1

open_canvas()
## image = load_image('character.png')   ## LEC04
gra = load_image('grass.png')
run = load_image('run_animation.png')

running = True
## x = 0    ## LEC05
x = 800 // 2
frame = 0
dir = 0
while running:
    clear_canvas_now()
    gra.draw_now(400, 30)
    ## image.draw_now(x, 90)     ## LEC04
    run.clip_draw(frame * 100, 0, 100, 100, x, 90)
    update_canvas()
    handle_events()
    frame = (frame + 1) % 8
    x += dir * 5
    delay(0.05)
    ## get_events()     ## LEC06

close_canvas()


