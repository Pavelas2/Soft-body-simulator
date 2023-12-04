import math
import itertools as it

Y_module = 0.01


def distance(body1, body2):
    return math.sqrt((body1.x - body2.x) ** 2 + (body1.y - body2.y) ** 2)


def calculate_force(parts):
    indifferent_dist = 100
    for pair in it.combinations(parts, 2):
        d = (distance(pair[0], pair[1]) - indifferent_dist)
        if d:
            F = d * Y_module
            pair[0].Fx += (pair[1].x - pair[0].x) / abs(d) * F
            pair[0].Fy += (pair[1].y - pair[0].y) / abs(d) * F
            pair[1].Fx += (pair[0].x - pair[1].x) / abs(d) * F
            pair[1].Fy += (pair[0].y - pair[1].y) / abs(d) * F

