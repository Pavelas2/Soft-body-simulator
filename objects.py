from physic import *
import numpy as nm

class Particle:
    Fx = 0
    Fy = 0
    image = None

    def __init__(self, x, y, r, m=1, Vx=0, Vy=0, color='black'):
        self.x = x
        self.y = y
        self.r = r
        self.m = m
        self.Vx = Vx
        self.Vy = Vy
        self.color = color

    def move(self):
        self.Vx += self.Fx / self.m
        self.Vy += self.Fy / self.m
        self.x += self.Vx
        self.y += self.Vy
        self.Fx = 0
        self.Fy = 0.5
        self.Vx *= 0.85
        self.Vy *= 0.85

        if self.x >= 600:
            self.x = 600
            self.Vx *= -0.9
        if self.x <= 0:
            self.x = 0
            self.Vx *= -0.9
        if self.y >= 600:
            self.y = 600
            self.Vy *= -0.9
        if self.y <= 0:
            self.y = 0
            self.Vx *= -0.9

    def connect_particles(self, parts):
        self.conn += parts


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

    def __init__(self, parts):
        self.parts = parts
        self.indifferent_dist = distance(parts[0], parts[1])

    def calculate_parts_force(self):
        d = (distance(self.parts[0], self.parts[1]) - self.indifferent_dist)
        if d:
            F = d * self.Y_module + d/200*(d*Y_module)**2
            print(self.parts[0].Fx, (self.parts[1].x - self.parts[0].x))
            self.parts[0].Fx += (self.parts[1].x - self.parts[0].x) / abs(d) * F
            self.parts[0].Fy += (self.parts[1].y - self.parts[0].y) / abs(d) * F
            self.parts[1].Fx += (self.parts[0].x - self.parts[1].x) / abs(d) * F
            self.parts[1].Fy += (self.parts[0].y - self.parts[1].y) / abs(d) * F
            print(self.parts[0].Fx)
