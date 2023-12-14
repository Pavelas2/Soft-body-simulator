import re
import tkinter
from pathlib import Path
from tkinter.messagebox import showinfo

from numpy.linalg import norm

from constants import *
from save import *
from visual import *

simulation_started = True

captured_part = None

mouse_pos = np.zeros(2)

def change_sim_status():
    if simulation_started:
        stop_sim()
    else:
        start_sim()

def start_sim():
    global simulation_started
    global root
    simulation_started = True

    start_button["text"] = "Stop"
    start_button["command"] = stop_sim

    simulation()


def stop_sim():
    global simulation_started
    simulation_started = False

    start_button["text"] = "Start"
    start_button["command"] = start_sim


def simulation():
    for body in bodies:
        body.update_pos(DT, 5)
        update_body_image(space, body)

    move_captured_part()

    if simulation_started:
        space.after(10, simulation)


def save_data():
    for path in Path("./bodydata").glob('*'):
        os.remove(path)
    for body in bodies:
        save_body_data(body.name, body)


def reset():
    global bodies
    global body_listbox

    delete(space, bodies)

    bodies = []

    for path in Path("./bodydata").glob('*'):
        name = re.search(r"/([a-zA-Z0-9_.+-]*)([\s_a-zA-Z0-9.+-]*)([a-zA-Z0-9-]*)[.]+", str(path))[0][1:-1]
        parts, connects = load_body_data(str(path))
        bodies.append(Body(parts=parts, connects=connects, name=name))

    for body in bodies:
        create_body_image(space, body)
    for block in blocks:
        create_block_image(space, block)

    body_listbox['listvariable'] = tkinter.Variable(value=[x.name for x in bodies])


def mouse_down(event):
    global captured_part
   # global grab
    global button_value
    #global adding_part
    #global adding_con
    if button_value.get() in [1, 3]:
    #if adding_con.get() or grab.get():
        capture_part(event)
    elif button_value.get() == 2 and body_listbox.curselection():
        add_part(event)


def is_point_on_part(event, part):
    return ((part.pos[0] - 1.5 * part.r <= event.x <= part.pos[0] + 1.5 * part.r)
            and (part.pos[1] - 1.5 * part.r <= event.y <= part.pos[1] + 1.5 * part.r))


def capture_part(event):
    global captured_part
    if not captured_part:
        for body in bodies:
            for part in body.parts:
                if is_point_on_part(event, part):
                    captured_part = part
                    break


def add_part(event):
    body = bodies[body_listbox.curselection()[0]]
    new_part = Particle(len(body.parts), np.array([event.x, event.y], dtype=float), 5, V=np.zeros(2, float))
    create_part_image(space, new_part)
    body.parts.append(new_part)


def add_connection(event):
    global button_value
    connection_added = False
    if button_value.get() == 3 and body_listbox.curselection():
        body = bodies[body_listbox.curselection()[0]]
        for part in body.parts:
            if is_point_on_part(event, part):
                if captured_part in body.parts and part in body.parts and not connection_added:
                    new_connect = Connection(part, captured_part)
                    create_connection_image(space, new_connect)
                    body.connects.append(new_connect)
                    connection_added = True


def mouse_up(event):
    global captured_part
    add_connection(event)
    captured_part = None


def mouse_move(event):
    global mouse_pos
    mouse_pos = np.array([event.x, event.y])


def check_selection(event):
    if body_listbox.curselection():
        for body in bodies:
            body.chosen = False
        bodies[body_listbox.curselection()[0]].chosen = True


def move_captured_part():
    global mouse_pos
    global button_value
    if captured_part and button_value.get() != 3:
        r_vector = mouse_pos - captured_part.pos
        captured_part.F += 0.8*(r_vector - 1/10*captured_part.V) / norm(r_vector) * min([50, 1.8 ** np.linalg.norm(r_vector)])


def add_body():
    new_name = new_body_entry.get()
    if new_name not in body_listbox.get(0, body_listbox.size()):
        new_body = Body(new_name)
        bodies.append(new_body)
        body_listbox.insert(body_listbox.size(), new_body.name)
    else:
        showinfo(title="Info", message="Name already in use")

def space_pressed(event):
    if start_button["text"] == "Start":
        start_sim()
    else:
        stop_sim()

def main():
    global root
    global start_button
    global space
    global body_listbox
    global new_body_entry

    global grab_button
    global grab

    global button_value
    #global add_part_button
    #global adding_part

    #global adding_con

    root = tkinter.Tk()
    root.title("Soft-body")
    root.bind('<space>', lambda event: change_sim_status())
    root.bind('<r>', lambda event: reset())

    # пространство отображается на холсте типа Canvas
    space = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    space.bind('<Button-1>', mouse_down)
    space.bind('<Motion>', mouse_move)
    space.bind('<ButtonRelease-1>', mouse_up)

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
    root.bind('<space>', space_pressed)

    save_button = tkinter.Button(frame, text="Save", command=save_data)
    save_button.grid(row=3, column=1)

    reset_button = tkinter.Button(frame, text="Reset", command=reset)
    reset_button.grid(row=4, column=1)
    # start_button.bind('<Button-1>', start_sim)
    # start_button.pack(side=tkinter.RIGHT)

    new_body_entry = tkinter.Entry(frame)
    new_body_entry.grid(column=0, row=0, padx=3, pady=6, sticky=tkinter.EW)
    tkinter.Button(frame, text="Add body", command=add_body).grid(column=1, row=0, padx=6, pady=6)

    # создаем список
    body_listbox = tkinter.Listbox(frame, height=5, width=10,
                                   listvariable=tkinter.Variable(value=[x.name for x in bodies]))
    body_listbox.bind("<<ListboxSelect>>", check_selection)
    body_listbox.grid(row=1, column=0, columnspan=2, sticky=tkinter.EW, padx=5, pady=5)

    button_value = tkinter.IntVar()
    grab = tkinter.IntVar(value=0)
    grab_button = tkinter.Radiobutton(frame, text="Grab particle", variable=button_value, value=1)
    grab_button.grid()

    #adding_part = tkinter.IntVar(value=0)
    add_part_button = tkinter.Radiobutton(frame, text="Add particle", variable=button_value, value=2)
    add_part_button.grid()

    #adding_con = tkinter.IntVar(value=0)
    adding_con_button = tkinter.Radiobutton(frame, text="Add connection", variable=button_value, value=3)
    adding_con_button.grid()

    # reset()

    for body in bodies:
        create_body_image(space, body)

    for block in blocks:
        create_block_image(space, block)

    start_sim()

    root.mainloop()


if __name__ == '__main__':
    make_bounds()
    main()
