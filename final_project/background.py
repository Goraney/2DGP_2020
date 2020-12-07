import gfw
from pico2d import *
from gobj import *

class Background:
    def __init__(self, imageName):
        self.imageName = imageName
        self.image = gfw.image.load((imageName))
        self.target = None
        self.cw, self.ch = get_canvas_width(), get_canvas_height()
        self.win_rect = 0, 0, self.cw, self.ch
        self.center = self.image.w // 2, self.image.h // 2

    def draw(self):
        self.image.clip_draw_to_origin(*self.win_rect, 0, 0)

    def update(self):
        if self.target is None:
            return
        tx, ty = self.target.pos
        sl = round(tx - self.cw / 2)
        sb = round(ty - self.ch / 2)
        self.win_rect = sl, sb, self.cw, self.ch