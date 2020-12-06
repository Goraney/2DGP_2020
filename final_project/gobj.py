from pico2d import *
import gfw
import threading

count = 0

def point_check(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    if x1 < x2: return True
    elif x1 >= x2: return False

def collides_box(a, b):
    (la, ba, ra, ta) = a.get_bb()
    (lb, bb, rb, tb) = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ba > tb: return False
    if ta < bb: return False

    return True

def distance_sq(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

def distance(point1, point2):
    if math.sqrt(distance_sq(point1, point2)) > 48: return False

    return True

def pt_in_rect(point, rect):
    (x, y) = point
    (l, b, r, t) = rect

    if x < l: return False
    if x > r: return False
    if y < b: return False
    if y > t: return False

    return True

def draw_collision_box():
    for obj in gfw.world.all_objects():
        if hasattr(obj, 'get_bb'):
            draw_rectangle(*obj.get_bb())

def hit_timer():
    global count
    timer = threading.Timer(0.5, hit_timer)
    timer.start()
    count += 0.5
    if count > 1.5:
        timer.cancel()


if __name__ == "__main__":
    print("This file is not supposed to be executed directly.")