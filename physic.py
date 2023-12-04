import numpy as np

DT = 1


def perpendicular_to_line(point: np.array, line: np.array):  # line shape = (2, 2), two points
    n = (line[1] - line[0]) / np.linalg.norm((line[1] - line[0]))
    perpendicular = line[0] - point - ((line[0] - point) @ n) * n
    return perpendicular


def min_by_module(list):
    min_vector = list.pop()
    for vector in list:
        if np.linalg.norm(vector) < np.linalg.norm(min_vector):
            min_vector = vector
    return min_vector


def intersection_of_border(point1, point2, point3, point4):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x4, y4 = point4

    if (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4):

        x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
                (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
                (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

        if (((x3 <= x <= x4) or (x3 >= x >= x4)) and ((y3 <= y <= y4) or (y3 >= y >= y4))) and (((x1 <= x <= x2) or (x1 >= x >= x2)) and ((y1 <= y <= y2) or (y1 >= y >= y2))) :
            return True
    return False


def collision(part, block):
    n = 0
    for i in range(len(block.points)):
        if intersection_of_border(part.pos, [0,0], *(block.points + [block.points[0]])[i:i + 2:1]):
            n += 1



    if n % 2:
        list_of_perpendicular = []
        for i in range(len(block.points)):
            list_of_perpendicular.append(perpendicular_to_line(part.pos, np.array([*(block.points + [block.points[0]])[i:i + 2:1]])))
        print(list_of_perpendicular)
        vector = min_by_module(list_of_perpendicular)
        print(part.pos, vector)
        part.pos += vector
        print(part.pos)
        part.V -= 2 * (part.V @ vector / (np.linalg.norm(vector) or 1)) * vector / (np.linalg.norm(vector) or 1)
