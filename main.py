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
N = 3

mouse_pos = np.zeros(2)

blocks.append(Block([[-200, window_height - 10], [window_width + 200, window_height - 10],
                     [window_width + 200, window_height + 200],[-200, window_height + 200]]))
blocks.append(Block([[-200, 10], [window_width + 200, 10], [window_width + 200, -250], [-100, -250]]))
blocks.append(Block([[window_width - 10, -100], [window_width + 100, -100],
                     [window_width + 100, window_height + 100],[window_width - 10, window_height + 100]]))
blocks.append(Block([[-100, -100], [10, -100], [10, window_height+100], [-100, window_height+100]]))
blocks.append(Block([[300, 600], [500, 400], [500, 600]]))

blocks.append(Block([[0, 300], [0, 280], [300, 280], [300, 300]]))
"""
parts = [Particle(0, np.array([window_width / 2, window_height / 2]), 5, color="blue", V=np.array([-0., 5.])),
         Particle(1, np.array([window_width / 2 + 50, window_height / 2]), 5, color="red", V=np.array([0., 0.])),
         Particle(2, np.array([window_width / 2 + 50, window_height / 2 + 50]), 5, color="green", V=np.array([0., 0.])),
         Particle(3, np.array([window_width / 2, window_height / 2 + 50]), 5),
         Particle(4, np.array([window_width / 2 + 25, window_height / 2 + 25]), 5)]

connects = [Connection((parts[0], parts[1])),
            Connection((parts[0], parts[3])),
            Connection((parts[0], parts[4])),
            Connection((parts[1], parts[2])),
            Connection((parts[1], parts[4])),
            Connection((parts[2], parts[3])),
            Connection((parts[2], parts[4])),
            Connection((parts[3], parts[4]))]
"""

#bodies.append(Body(connects=connects, parts=parts))
#save_body_data(bodies[0].name, parts, connects)

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
        body.update_pos(DT, 2)
        update_body_image(space, body)

    move_captured_part()

    if simulation_started:
        space.after(10, simulation)

def save_data():
    for body in bodies:
        save_body_data(body.name, body.parts, body.connects)

def reset():
    global bodies
    stop_sim()
    delete(space, bodies[0])
    for body in bodies:
        parts, connects = load_body_data('Body1')
        body.parts = parts
        body.connects = connects
    space.after(10, start_sim)

def mousedown(event):
    global captured_part
    n = 4
    if not captured_part:
        for body in bodies:
            for part in body.parts:
                if ((part.pos[0] - n * part.r <= event.x <= part.pos[0] + n * part.r)
                        and (part.pos[1] - n * part.r <= event.y <= part.pos[1] + n * part.r)):
                    captured_part = part
                    print(captured_part)
                    break


def mouseup(event):
    global captured_part
    captured_part = None


def mousemove(event):
    global mouse_pos
    mouse_pos = np.array([event.x, event.y])

def move_captured_part():
    global mouse_pos
    if captured_part:
        r_vector = mouse_pos - captured_part.pos
        captured_part.F += r_vector / np.linalg.norm(r_vector) * min([5 ,(math.exp(np.linalg.norm(r_vector)/15)-1)/10])

def main():
    global start_button
    global space

    parts, connects = load_body_data('Body1')
    bodies.append(Body(connects=connects, parts=parts))

    root = tkinter.Tk()
    root.title("Soft-body")
    # пространство отображается на холсте типа Canvas
    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="white")
    space.bind('<Button-1>', mousedown)
    space.bind('<Motion>', mousemove)
    space.bind('<ButtonRelease-1>', mouseup)
    space.pack(side=tkinter.LEFT)
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.RIGHT)

    start_button = tkinter.Button(frame, text="Start", command=start_sim)
    start_button.pack()

    save_button = tkinter.Button(frame, text="Save", command=save_data)
    save_button.pack()

    reset_button = tkinter.Button(frame, text="Reset", command=reset)
    reset_button.pack()
    # start_button.bind('<Button-1>', start_sim)
    # start_button.pack(side=tkinter.RIGHT)


    start_sim()

    root.mainloop()


if __name__ == '__main__':
    main()
