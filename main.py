import tkinter

import numpy as np

from save import *
from visual import *
from physic import *
from objects import *
import itertools as it

simulation_started = True

bodies = []

blocks.append(Block([[-100, window_height-20], [window_width+100, window_height-20], [window_width+100, window_height+50], [-100, window_height+50]]))
blocks.append(Block([[-100, 20], [window_width+100, 20], [window_width+100, -50], [-100, -50]]))
blocks.append(Block([[window_width-20, -30], [window_width+20, -30],[window_width+20, window_height+30], [window_width-20, window_height+30]] ))
blocks.append(Block([[-100, -30], [20, -30],[20, 630], [-100, 630]] ))
blocks.append(Block([[300, 550], [500, 400], [500,550]]))


parts = [Particle(np.array([window_width/2, window_height/2]), 5, color="blue", V=np.array([-0., 5.])),
         Particle(np.array([window_width/2+50, window_height/2]), 5, color="red", V=np.array([0., 0.])),
         Particle(np.array([window_width/2+50, window_height/2+50]), 5, color="green", V=np.array([0., 0.])),
         Particle(np.array([window_width/2, window_height/2+50]), 5),
         Particle(np.array([window_width/2+25, window_height/2+25]), 5)]

connects = [Connection((parts[0], parts[1])),
            Connection((parts[0], parts[3])),
            Connection((parts[0], parts[4])),
            Connection((parts[1], parts[2])),
            Connection((parts[1], parts[4])),
            Connection((parts[2], parts[3])),
            Connection((parts[2], parts[4])),
            Connection((parts[3], parts[4]))]


bodies.append(Body(connects=connects, parts=parts))


def start_sim():
    global simulation_started
    simulation_started = True

    start_button["text"] = "Stop"
    start_button["command"] = stop_sim

    for body in bodies:
        create_body_image(space, body)

    for block in blocks:
        create_block_image(space, block)

    space.create_oval(-10, -10, 10, 10)
    simulation()


def stop_sim():
    global simulation_started
    simulation_started = False

    start_button["text"] = "Start"
    start_button["command"] = start_sim


def simulation():
    for body in bodies:
        body.update_pos(DT, 1)
        update_body_image(space, body)

    if simulation_started:
        space.after(10, simulation)


def main():
    global start_button
    global space

    root = tkinter.Tk()
    root.title("Soft-body")
    # пространство отображается на холсте типа Canvas
    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="white")
    space.pack(side=tkinter.LEFT)
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.RIGHT)

    start_button = tkinter.Button(frame, text="Start", command=start_sim)
    start_button.pack(side=tkinter.BOTTOM)

    start_sim()

    root.mainloop()


if __name__ == '__main__':
    main()
