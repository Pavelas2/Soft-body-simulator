import numpy as np


def perpendicular_to_line(point: np.ndarray, line: np.ndarray):
    """Находит перпендикуляр от точки до прямой"""
    n = (line[1] - line[0]) / np.linalg.norm((line[1] - line[0]))
    perpendicular = line[0] - point - ((line[0] - point) @ n) * n
    return perpendicular


def min_by_module(list_of_vectors):
    """Возвращает вектор наименьшей длинны"""
    min_vector = list_of_vectors.pop()
    for vector in list_of_vectors:
        if np.linalg.norm(vector) < np.linalg.norm(min_vector):
            min_vector = vector
    return min_vector


def intersection_of_border(point1, point2, point3, point4):
    """Отслеживает пересечение двух прямых"""
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x4, y4 = point4

    if (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4):

        x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
                (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
                (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

        if (((x3 <= x <= x4) or (x3 >= x >= x4)) and ((y3 <= y <= y4) or (y3 >= y >= y4))) and (
                ((x1 <= x <= x2) or (x1 >= x >= x2)) and ((y1 <= y <= y2) or (y1 >= y >= y2))):
            return True
    return False


def collision(part, block):
    """Обрабатывает столкновения с препятствиями"""
    n = 0
    for i in range(len(block.points)):
        if intersection_of_border(part.pos, [-1000, -1000], *(block.points + [block.points[0]])[i:i + 2:1]):
            n += 1

    k = 0

    for i in range(len(block.points)):
        if intersection_of_border(part.pos, [1000, 1000], *(block.points + [block.points[0]])[i:i + 2:1]):
            k += 1

    if n % 2 and k % 2:
        list_of_perpendicular = []
        for i in range(len(block.points)):
            list_of_perpendicular.append(
                perpendicular_to_line(part.pos, np.array([*(block.points + [block.points[0]])[i:i + 2:1]])))
        vector = min_by_module(list_of_perpendicular)
        part.pos += vector
        n = -(part.V @ vector / (np.linalg.norm(vector) or 1)) * vector / (np.linalg.norm(vector) or 1)
        parallel_v = part.V + n
        part.V = n * 0.8 + parallel_v * 0.95