import tkinter
from tkinter.messagebox import showinfo

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

blocks.append(Block([[-200, window_height - 10], [window_width + 200, window_height - 10],
                     [window_width + 200, window_height + 200], [-200, window_height + 200]]))
blocks.append(Block([[-200, 10], [window_width + 200, 10], [window_width + 200, -250], [-100, -250]]))
blocks.append(Block([[window_width - 10, -100], [window_width + 100, -100],
                     [window_width + 100, window_height + 100], [window_width - 10, window_height + 100]]))
blocks.append(Block([[-100, -100], [10, -100], [10, window_height + 100], [-100, window_height + 100]]))
# blocks.append(Block([[300, 600], [500, 400], [500, 600]]))

parts = [Particle(np.array([window_width / 2, window_height / 2]), 5, V=np.array([0., 0.])),
         Particle(np.array([window_width / 2 + 50, window_height / 2]), 5, V=np.array([-0.0, 0.])),
         Particle(np.array([window_width / 2 + 50, window_height / 2 + 50]), 5, V=np.array([0., 0.])),
         Particle(np.array([window_width / 2, window_height / 2 + 50]), 5),
         Particle(np.array([window_width / 2 + 25, window_height / 2 + 25]), 5)]

connects = [Connection((parts[0], parts[1])),
            Connection((parts[0], parts[3])),
            Connection((parts[0], parts[4])),
            Connection((parts[1], parts[2])),
            Connection((parts[1], parts[4])),
            Connection((parts[2], parts[3])),
            Connection((parts[2], parts[4])),
            Connection((parts[3], parts[4]))]

bodies.append(Body("body 1", connects=connects, parts=parts))


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

    move_captured_part()

    check_selection()

    if simulation_started:
        space.after(10, simulation)


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
        new_part = Particle(np.array([event.x, event.y], dtype=float), 5)
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

    # текстовое поле и кнопка для добавления в список
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

    start_sim()

    root.mainloop()


if __name__ == '__main__':
    main()
