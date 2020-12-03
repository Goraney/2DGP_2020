from pico2d import *
import gfw

def point_add(point1, point2):
    x1,y1 = point1
    x2,y2 = point2
    return x1+x2, y1+y2

def collides_box(a, b):
	(la, ba, ra, ta) = a.get_bb()
	(lb, bb, rb, tb) = b.get_bb()

	if la > rb: return False
	if ra < lb: return False
	if ba > tb: return False
	if ta < bb: return False

	return True

def distance_sq(point1, point2):
    x1,y1 = point1
    x2,y2 = point2
    return (x1-x2)**2 + (y1-y2)**2

def distance(point1, point2):
	math.sqrt(distance_sq(point1, point2))

def pt_in_rect(point, rect):
    (x, y) = point
    (l, b, r, t) = rect

    if x < l: return False
    if x > r: return False
    if y < b: return False
    if y > t: return False

    return True

if __name__ == "__main__":
	print("This file is not supposed to be executed directly.")