class Particle():
    def __init__(self, x, y, r, connections=[]):
        self.x = x
        self.y = y
        self.r = r
        self.conn = connections

    Vx = 0
    Vy = 0


class Body():
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
