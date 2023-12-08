import tkinter

import numpy as np

from save import *
from visual import *
from physic import *
from objects import *
import itertools as it

simulation_started = True

bodies = []
captured_part = None

blocks.append(Block([[-100, window_height-20], [window_width+100, window_height-20], [window_width+100, window_height+50], [-100, window_height+50]]))
blocks.append(Block([[-100, 20], [window_width+100, 20], [window_width+100, -50], [-100, -50]]))
blocks.append(Block([[window_width-20, -30], [window_width+20, -30],[window_width+20, window_height+30], [window_width-20, window_height+30]] ))
blocks.append(Block([[-100, -30], [20, -30],[20, 630], [-100, 630]] ))
blocks.append(Block([[300, 600], [500, 400], [500,600]]))


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

def mousedown(event):
    global captured_part, cursor
    n = 4
    #print(event.x, event.y)
    if captured_part is None:
        for body in bodies:
            for part in body.parts:
                if (part.pos[0] - n*part.r <= event.x <= part.pos[0] + n*part.r) and (part.pos[1] - n*part.r <= event.y <= part.pos[1] + n*part.r):
                    part.captured = True
                    captured_part = part
                    cursor = Cursor(np.array([event.x, event.y]))

def mouseup(event):
    global captured_part
    if captured_part is not None:
        captured_part.captured = False
        captured_part = None

def mousemove(event):
    global captured_part, cursor
    
    if captured_part is not None:
        cursor.update(np.array([event.x, event.y])) ##change later to dt based on fps rate
        #calculate_fict_force(captured_part, cursor.a)
        #print(captured_part.pos)
        #translate(bodies[0], cursor.pos - cursor.prev_pos)
        translate(bodies[0], np.array([event.x, event.y]) - captured_part.pos)

def main():
    global start_button
    global space

    root = tkinter.Tk()
    root.title("Soft-body")
    # пространство отображается на холсте типа Canvas
    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="white")
    space.bind('<Button-1>', mousedown)
    space.bind('<B1-Motion>', mousemove)
    space.bind('<ButtonRelease-1>', mouseup)
    space.pack(side=tkinter.LEFT)
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.RIGHT)

    start_button = tkinter.Button(frame, text="Start", command=start_sim)
    start_button.pack()
    #start_button.bind('<Button-1>', start_sim)
    #start_button.pack(side=tkinter.RIGHT)


    start_sim()

    root.mainloop()


if __name__ == '__main__':
    main()
