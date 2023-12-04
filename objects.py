from physic import *
from visual import window_width, window_height
import numpy as np
from physic import *


class Particle:
    F = np.zeros(2)
    image = None

    def __init__(self, pos: np.array, r, m=1, V=np.zeros(2), color='black'):
        self.pos = pos
        self.V = V
        self.r = r
        self.m = m
        self.color = color

    def move(self, dt):
        self.V += self.F / self.m * dt
        self.pos += self.V * dt
        self.F = np.zeros(2)


class Body:
    def __init__(self, connects=[], parts=[]):
        self.connects = connects
        self.parts = parts

    def update_pos(self, dt, N):
        for i in range(N):
            self.update_force()
            for part in self.parts:
                part.move(dt / N)
                for block in blocks:
                    collision(part, block)

    def update_force(self):
        for part in self.parts:
            part.F = np.array([0., 0.1])
        for connect in self.connects:
            connect.calculate_parts_force()


class Connection:
    k = 0.09
    k_d = 0.08

    image = None

    def __init__(self, parts):
        self.parts = parts
        self.eq_dist = np.linalg.norm(self.parts[0].pos - self.parts[1].pos)

    def calculate_parts_force(self):
        if not self.parts[0] == self.parts[1]:
            r_vector = self.parts[1].pos - self.parts[0].pos
            v_vector = self.parts[1].V - self.parts[0].V
            d = np.linalg.norm(r_vector)
            delta_d = d - self.eq_dist
            self.parts[0].F += (delta_d * self.k + (r_vector / d) @ v_vector * self.k_d) * r_vector / d
            self.parts[1].F -= (delta_d * self.k + (r_vector / d) @ v_vector * self.k_d) * r_vector / d


class Block:
    image = None

    def __init__(self, points):
        self.points = points


blocks = []