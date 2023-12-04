from physic import *
from visual import window_width, window_height
import numpy as np

DT = 0.1

class Particle:
    F = np.zeros(2)
    image = None

    def __init__(self, m, r, x: np.ndarray, v: np.ndarray, color='black'):
        self.x = x
        self.r = r
        self.m = m
        self.v = v
        self.color = color

    def move(self):
        self.v += self.F * DT / self.m
        self.x += self.v * DT
        self.F = np.array([0, 0.5])

        if self.x >= window_width:
            self.x = window_width
            self.Vx *= -0.9
        if self.x <= 0:
            self.x = 0
            self.Vx *= -0.9
        if self.y >= window_height:
            self.y = window_height
            self.Vy *= -0.9
        if self.y <= 0:
            self.y = 0
            self.Vx *= -0.9


class Body:
    def __init__(self, connects=[], parts=[]):
        self.connects = connects
        self.parts = parts

    def update_pos(self):
        for i in range(1):
            self.update_force()
            self.move()

    def move(self):

        for part in self.parts:
            part.move()

    def update_force(self):
        for connect in self.connects:
            connect.calculate_parts_force()
        #calculate_force(self.parts)

class Connection:
    Y_module = 0.01  # Модуль Юнга
    image = None

    def __init__(self, *parts):
        self.parts = parts
        self.eq_dist = distance(parts[0], parts[1])

    def calculate_parts_force(self):
        d = (distance(self.parts[0], self.parts[1]) - self.eq_dist)
        if d:
            F = d * self.Y_module + d/200*(d*Y_module)**2
            print(self.parts[0].Fx, (self.parts[1].x - self.parts[0].x))
            self.parts[0].Fx += (self.parts[1].x - self.parts[0].x) / abs(d) * F
            self.parts[0].Fy += (self.parts[1].y - self.parts[0].y) / abs(d) * F
            self.parts[1].Fx += (self.parts[0].x - self.parts[1].x) / abs(d) * F
            self.parts[1].Fy += (self.parts[0].y - self.parts[1].y) / abs(d) * F
            print(self.parts[0].Fx)
