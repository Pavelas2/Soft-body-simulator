import math
from constants import *
from numpy.linalg import norm

from physic import *


class Particle:
    F = np.zeros(2)
    image = None
    type = "basic"

    def __init__(self, number, pos: np.ndarray, r, m=1, V=np.zeros(2), color='black'):
        self.number = number
        self.pos = pos
        self.V = V
        self.r = r
        self.m = m
        self.color = color
        self.captured = False

    def move(self, dt):
        self.V += self.F / self.m * dt
        self.pos += self.V * dt

    def self_collision(self, parts):
        for part in [x for x in parts if x != self]:
            r_vector = part.pos - self.pos
            if np.linalg.norm(r_vector) <= self.r + part.r:
                if part.type == 'basic':
                    part.pos += r_vector / 2 * 0.9
                self.pos -= r_vector / 2 * 0.9
                V1 = np.linalg.norm(self.V)
                V2 = np.linalg.norm(part.V)
                A1 = math.atan2(self.V[1], self.V[0])
                A2 = math.atan2(part.V[1], part.V[0])
                phi = math.atan2(r_vector[1], r_vector[0])
                m1 = self.m
                m2 = part.m
                V1x = ((V1 * math.cos(A1 - phi) * (m1 - m2) + 2 * m2 * V2 * math.cos(A2 - phi)) / (m1 + m2) * math.cos(
                    phi)
                       + V1 * math.sin(A1 - phi) * math.cos(phi + math.pi / 2))
                V1y = ((V1 * math.cos(A1 - phi) * (m1 - m2) + 2 * m2 * V2 * math.cos(A2 - phi)) / (m1 + m2) * math.sin(
                    phi)
                       + V1 * math.sin(A1 - phi) * math.sin(phi + math.pi / 2))
                V2x = ((V2 * math.cos(A2 - phi) * (m2 - m1) + 2 * m1 * V1 * math.cos(A1 - phi)) / (m1 + m2) * math.cos(
                    phi)
                       + V2 * math.sin(A2 - phi) * math.cos(phi + math.pi / 2))
                V2y = ((V2 * math.cos(A2 - phi) * (m2 - m1) + 2 * m1 * V1 * math.cos(A1 - phi)) / (m1 + m2) * math.sin(
                    phi)
                       + V2 * math.sin(A2 - phi) * math.sin(phi + math.pi / 2))

                self.V = np.array([V1x, V1y])
                part.V = np.array([V2x, V2y])

            if norm(r_vector) <= 60:
                F = 1 / 5 * r_vector / ((norm(r_vector) / 2) ** 2)
                # self.F -= F


class Body:
    chosen = False

    def __init__(self, name="body 1", connects=[], parts=[]):
        self.name = name
        self.connects = connects
        self.parts = parts

    def update_pos(self, dt, N):
        for i in range(N):
            self.update_force()
            for part in self.parts:
                #part.self_collision(self.parts)
                part.move(dt / N)
                for block in blocks:
                    collision(part, block)
                part.F = np.zeros(2)

    def update_force(self):
        for part in self.parts:
            part.F += np.array([0., 0.2])
        for connect in self.connects:
            connect.calculate_parts_force()


class Connection:
    k = 0.01
    k_d = 0.2

    image = None

    def __init__(self, *parts):
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


class Static_part(Particle):
    type = "static"

    def __init__(self, number, pos: np.ndarray, r, m=1, V=np.zeros(2), color='black'):
        Particle.__init__(self, number, pos, r, m=1, V=np.zeros(2), color='black')

    def move(self, dt):
        ...

    def self_collision(self, parts):
        ...

blocks = []
bodies = []


def make_bounds():
    blocks.append(
        Block([[-100, HEIGHT - 20], [WIDTH + 100, HEIGHT - 20], [WIDTH + 100, HEIGHT + 100], [-100, HEIGHT + 100]]))
    blocks.append(Block([[-100, 20], [WIDTH + 100, 20], [WIDTH + 100, -100], [-100, -100]]))
    blocks.append(Block([[WIDTH - 20, -50], [WIDTH + 100, -50], [WIDTH + 100, HEIGHT + 50], [WIDTH - 20, HEIGHT + 50]]))
    blocks.append(Block([[-100, -30], [20, -30], [20, 630], [-100, 630]]))
    # blocks.append(Block([[300, 600], [500, 400], [500, 600]]))
    # blocks.append(Block([[0, 300], [0, 280], [300, 280], [300, 300]]))
