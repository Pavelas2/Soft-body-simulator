import os
from objects import *

def load_body_data(filename):
    filepath = os.path.join('bodydata', filename + '.txt')
    with open (filepath, 'r') as f:
        parts = []
        connects = []
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i].split()
            if line[0] == 'p':
                pos = np.array([float(line[1]), float(line[2])])
                r = int(line[3])
                color = line[4]
                v = np.array([float(line[5]), float(line[6])])
                parts.append(Particle(i, pos, r=r, V=v, color=color))

            elif line[0] == 'c':
                connects.append(Connection(parts[int(line[1])], parts[int(line[2])]))

    return parts, connects
    

def save_body_data(filename, parts, connects):
    filepath = os.path.join('bodydata', filename + '.txt')
    with open(filepath, 'w') as f:
        for part in parts:
            line = "p %d %d %d %s %d %d\n" % (part.pos[0], part.pos[1], part.r, part.color, part.V[0], part.V[1])
            f.write(line)

        for connect in connects:
            line = "c %d %d\n" % (connect.parts[0].number, connect.parts[1].number)
            f.write(line)
