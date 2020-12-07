from pico2d import *
import gfw
from player import *

def load():
    global icon, bar, red, yellow, green, blue, icon_a, icon_s, icon_d, icon_z
    icon = gfw.image.load('res/stats_icon.png')
    bar = gfw.image.load('res/stats_bar.png')
    red = gfw.image.load('res/stats_gauge_red.png')
    yellow = gfw.image.load('res/stats_gauge_yellow.png')
    green = gfw.image.load('res/stats_gauge_green.png')
    blue = gfw.image.load('res/stats_gauge_blue.png')
    icon_a = gfw.image.load('res/skill_icon_a.png')
    icon_s = gfw.image.load('res/skill_icon_s.png')
    icon_d = gfw.image.load('res/skill_icon_d.png')
    icon_z = gfw.image.load('res/skill_icon_z.png')

def draw(player):
    load()
    rate_0 = player.stats_0 / player.max_stats
    rate_1 = player.stats_1 / player.max_stats
    rate_2 = player.stats_2 / player.max_stats
    rate_3 = player.stats_3 / player.max_stats

    icon.clip_draw(0, 0, 32, 128, 24, 72)
    bar.clip_draw(0, 0, 128, 128, 104, 72)
    red.clip_draw_to_origin(0, 0, round(128 * rate_0), 32, 40, 104)
    yellow.clip_draw_to_origin(0, 0, round(128 * rate_1), 32, 40, 72)
    green.clip_draw_to_origin(0, 0, round(128 * rate_2), 32, 40, 40)
    blue.clip_draw_to_origin(0, 0, round(128 * rate_3), 32, 40, 8)
    if rate_0 > 0.50:
        icon_a.clip_draw(0, 0, 32, 32, 104 + 72 + 8, 104 + 16)
    else:
        icon_a.clip_draw(32, 0, 32, 32, 104 + 72 + 8, 104 + 16)
    if rate_1 > 0.50:
        icon_s.clip_draw(0, 0, 32, 32, 104 + 72 + 8, 72 + 16)
    else:
        icon_s.clip_draw(32, 0, 32, 32, 104 + 72 + 8, 72 + 16)
    if rate_2 > 0.50:
        icon_d.clip_draw(0, 0, 32, 32, 104 + 72 + 8, 40 + 16)
    else:
        icon_d.clip_draw(32, 0, 32, 32, 104 + 72 + 8, 40 + 16)
    if rate_3 > 0.50:
        icon_z.clip_draw(0, 0, 32, 32, 104 + 72 + 8, 8 + 16)
    else:
        icon_z.clip_draw(32, 0, 32, 32, 104 + 72 + 8, 8 + 16)

