import tkinter
from tkinter.messagebox import showinfo
from pathlib import Path
import re

import numpy as np

from save import *
from visual import *
from physic import *
from objects import *
import itertools as it

simulation_started = True

grab = None
bodies = []
captured_part = None
N = 3

mouse_pos = np.zeros(2)

blocks.append(Block([[-100, window_height - 20], [window_width + 100, window_height - 20],
                     [window_width + 100, window_height + 50], [-100, window_height + 50]]))
blocks.append(Block([[-100, 20], [window_width + 100, 20], [window_width + 100, -50], [-100, -50]]))
blocks.append(Block([[window_width - 20, -30], [window_width + 20, -30],
                     [window_width + 20, window_height + 30], [window_width - 20, window_height + 30]]))
blocks.append(Block([[-100, -30], [20, -30], [20, 630], [-100, 630]]))
blocks.append(Block([[300, 600], [500, 400], [500, 600]]))
blocks.append(Block([[0, 300], [0, 280], [300, 280], [300, 300]]))


parts = [Particle(0, np.array([window_width / 2, window_height / 2]), 5, color="blue", V=np.array([-0., 5.])),
         Particle(1, np.array([window_width / 2 + 50, window_height / 2]), 5, color="red", V=np.array([0., 0.])),
         Particle(2, np.array([window_width / 2 + 50, window_height / 2 + 50]), 5, color="green", V=np.array([0., 0.])),
         Particle(3, np.array([window_width / 2, window_height / 2 + 50]), 5),
         Particle(4, np.array([window_width / 2 + 25, window_height / 2 + 25]), 5)]

connects = [Connection(parts[0], parts[1]),
            Connection(parts[0], parts[3]),
            Connection(parts[0], parts[4]),
            Connection(parts[1], parts[2]),
            Connection(parts[1], parts[4]),
            Connection(parts[2], parts[3]),
            Connection(parts[2], parts[4]),
            Connection(parts[3], parts[4])]



bodies.append(Body(connects=connects, parts=parts))
# save_body_data(bodies[0].name, parts, connects)

def start_sim():
    global simulation_started
    simulation_started = True

    start_button["text"] = "Stop"
    start_button["command"] = stop_sim

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

    move_captured_part()

    check_selection()

    if simulation_started:
        space.after(10, simulation)


def save_data():
    for path in Path("./bodydata").glob('*'):
        os.remove(path)
    for body in bodies:
        save_body_data(body.name, body.parts, body.connects)


def reset():
    global bodies
    global body_listbox
    stop_sim()
    delete(space, bodies)

    bodies = []

    body_listbox['listvariable'] = tkinter.Variable(value=[])

    for path in Path("./bodydata").glob('*'):
        name = re.search(r"\\([a-zA-Z0-9_.+-]*)([\s_a-zA-Z0-9.+-]*)([a-zA-Z0-9-]*)[.]+", str(path))[0][1:-1]
        parts, connects = load_body_data(str(path))
        bodies.append(Body(parts=parts, connects=connects, name=name))

    for body in bodies:
        print(*body.parts, "\n", sep="\n")
        create_body_image(space, body)

    body_listbox['listvariable'] = tkinter.Variable(value=[x.name for x in bodies])

    for block in blocks:
        create_block_image(space, block)

    start_sim()


def mousedown(event):
    global captured_part
    global grab
    global add_part
    n = 4
    if grab.get():
        if not captured_part:
            for body in bodies:
                for part in body.parts:
                    if ((part.pos[0] - n * part.r <= event.x <= part.pos[0] + n * part.r)
                            and (part.pos[1] - n * part.r <= event.y <= part.pos[1] + n * part.r)):
                        captured_part = part
                        break
    elif add_part.get() and body_listbox.curselection():
        body = bodies[body_listbox.curselection()[0]]
        new_part = Particle(len(body.parts), np.array([event.x, event.y], dtype=float), 5)
        create_part_image(space, new_part)
        body.parts.append(new_part)


def mouseup(event):
    global captured_part
    captured_part = None


def mousemove(event):
    global mouse_pos
    mouse_pos = np.array([event.x, event.y])


def check_selection():
    if body_listbox.curselection():
        bodies[body_listbox.curselection()[0]].chosen = True
        for body in [x for x in bodies if x != bodies[body_listbox.curselection()[0]]]:
            body.chosen = False


def move_captured_part():
    global mouse_pos
    if captured_part:
        r_vector = mouse_pos - captured_part.pos
        captured_part.F += (r_vector / np.linalg.norm(r_vector) *
                            min([5, (math.exp(np.linalg.norm(r_vector) / 15) - 1) / 10]))


def add_body():
    new_name = new_body_entry.get()
    if not new_name in body_listbox.get(0, body_listbox.size()):
        new_body = Body(new_name)
        bodies.append(new_body)
        body_listbox.insert(body_listbox.size(), new_body.name)
    else:
        showinfo(title="Info", message="Body with this name already exist")


def main():
    global start_button
    global space
    global body_listbox
    global new_body_entry

    global grab_button
    global grab

    global add_part_button
    global add_part

    root = tkinter.Tk()
    root.title("Soft-body")

    # пространство отображается на холсте типа Canvas
    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="white")
    space.bind('<Button-1>', mousedown)
    space.bind('<Motion>', mousemove)
    space.bind('<ButtonRelease-1>', mouseup)
    space.pack(side=tkinter.LEFT)

    # панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.RIGHT)

    frame.columnconfigure(index=0, weight=2)
    frame.columnconfigure(index=1, weight=1)
    frame.rowconfigure(index=0, weight=1)
    frame.rowconfigure(index=1, weight=3)
    frame.rowconfigure(index=2, weight=1)

    start_button = tkinter.Button(frame, text="Start", command=start_sim)
    start_button.grid(row=3)

    save_button = tkinter.Button(frame, text="Save", command=save_data)
    save_button.grid(row=3, column=1)

    reset_button = tkinter.Button(frame, text="Reset", command=reset)
    reset_button.grid(row=4, column=1)
    # start_button.bind('<Button-1>', start_sim)
    # start_button.pack(side=tkinter.RIGHT)

    new_body_entry = tkinter.Entry(frame)
    new_body_entry.grid(column=0, row=0, padx=3, pady=6, sticky=tkinter.EW)
    tkinter.Button(frame, text="Добавить", command=add_body).grid(column=1, row=0, padx=6, pady=6)

    # создаем список
    body_listbox = tkinter.Listbox(frame, height=5, width=10,
                                   listvariable=tkinter.Variable(value=[x.name for x in bodies]))
    body_listbox.grid(row=1, column=0, columnspan=2, sticky=tkinter.EW, padx=5, pady=5)

    grab = tkinter.IntVar(value=0)
    grab_button = tkinter.Checkbutton(frame, text="Grab particular", variable=grab)
    grab_button.grid()

    add_part = tkinter.IntVar(value=0)
    add_part_button = tkinter.Checkbutton(frame, text="Add particular", variable=add_part, command=grab_button.deselect)
    add_part_button.grid()

    grab_button["command"] = add_part_button.deselect

    #reset()

    for body in bodies:
        create_body_image(space, body)

    for block in blocks:
        create_block_image(space, block)

    start_sim()

    root.mainloop()


if __name__ == '__main__':
    main()
