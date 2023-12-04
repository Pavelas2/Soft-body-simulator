from physic import *
import numpy as np

class Particle:
    F = np.zeros(2)
    image = None

    def __init__(self, pos: np.array, r, m=1, V=np.zeros(2), color='black'):
        self.pos = pos
        self.V = V
        self.r = r
        self.m = m
        self.color = color

    def move(self):
        print(self.V, self.F)
        self.V += self.F / self.m
        self.pos += self.V
        self.F = np.zeros(2)


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
    k = 0.01  # Модуль Юнга
    image = None

    def __init__(self, parts):
        self.parts = parts
        self.indifferent_dist = np.linalg.norm(self.parts[0].pos - self.parts[1].pos)

    def calculate_parts_force(self):
        r_vector = self.parts[1].pos - self.parts[0].pos
        d = np.linalg.norm(r_vector)
        delta_d = d - self.indifferent_dist
        self.parts[0].F += delta_d * self.k * r_vector/d
        self.parts[1].F -= delta_d * self.k * r_vector/d

