import re
import tkinter
from pathlib import Path
from tkinter.messagebox import showinfo, askyesno

from numpy.linalg import norm

from constants import *
from save import *
from visual import *

simulation_started = True

captured_part = None

mouse_pos = np.zeros(2)


def start_sim(init=False):
    """Начинает моделирование"""
    global simulation_started
    global root
    simulation_started = True

    if init:
        stop_sim()
        reset()
    else:
        start_button["text"] = "Stop"
        start_button["command"] = stop_sim
        button_value.set(1)

    simulation()


def stop_sim():
    """Останавливает моделирование"""
    global simulation_started
    simulation_started = False

    start_button["text"] = "Start"
    start_button["command"] = start_sim


def simulation():
    """Обработка физики"""
    for body in bodies:
        body.update_pos(DT, 5)
        update_body_image(space, body)

    move_captured_part()

    if simulation_started:
        space.after(10, simulation)


def save_data():
    """Сохраняет все тела"""
    for path in Path("./bodydata").glob('*'):
        os.remove(path)
    for body in bodies:
        save_body_data(body.name, body)


def reset():
    """Загружает тела"""
    global bodies
    global body_listbox

    delete(space, bodies)
    bodies = []

    for path in Path("./bodydata").glob('*'):
        name = re.search(r"(/|\\)([a-zA-Z0-9_.+-]*)([\s_a-zA-Z0-9.+-]*)([a-zA-Z0-9-]*)[.]+", str(path))[0][1:-1]
        parts, connects = load_body_data(str(path))
        bodies.append(Body(parts=parts, connects=connects, name=name))

    for body in bodies:
        create_body_image(space, body)
    for block in blocks:
        create_block_image(space, block)

    body_listbox['listvariable'] = tkinter.Variable(value=[x.name for x in bodies])

def hide_body(get_name=False):
    """Прячет тело"""
    global bodies
    global body_listbox

    for i in range(len(bodies)):
        if bodies[i].chosen:
            name = bodies[i].name
            if get_name:
                return name
            for connect in bodies[i].connects:
                space.delete(connect.image)
            for part in bodies[i].parts:
                space.delete(part.image)
            del bodies[i]
            break

def delete_body():
    """Удаляет тело"""
    name = hide_body(get_name=True)
    dialog = askyesno(message='Are you sure you want to delete "%s"?' % name)
    if dialog:
        hide_body()
        path = os.path.join('bodydata', name + '.txt')
    try:
        os.remove(path)
    except:
        pass

def mouse_down(event):
    """Обрабатывает нажатие мышки"""
    global captured_part
    global button_value
    space.focus_set()
    if button_value.get() in [1, 3]:
        capture_part(event)
    elif button_value.get() == 2 and body_listbox.curselection():
        add_part(event)


def is_point_on_part(event, part):
    """Проверяет нажатие на частицу"""
    return ((part.pos[0] - 1.5 * part.r <= event.x <= part.pos[0] + 1.5 * part.r)
            and (part.pos[1] - 1.5 * part.r <= event.y <= part.pos[1] + 1.5 * part.r))


def capture_part(event):
    """Захватывает частицу"""
    global captured_part
    if not captured_part:
        for body in bodies:
            for part in body.parts:
                if is_point_on_part(event, part):
                    captured_part = part
                    break


def add_part(event):
    """Добавляет частицу"""
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
        hide_button["state"] = 'normal'
        delete_button["state"] = 'normal'


def move_captured_part():
    global mouse_pos
    global button_value
    if captured_part and button_value.get() != 3:
        r_vector = mouse_pos - captured_part.pos
        captured_part.F += 0.8 * (r_vector - 1 / 10 * captured_part.V) / norm(r_vector) * min(
            [50, 1.8 ** np.linalg.norm(r_vector)])


def add_body():
    new_name = new_body_entry.get().strip()
    if new_name not in body_listbox.get(0, body_listbox.size()) and new_name:
        new_body = Body(new_name)
        bodies.append(new_body)
        body_listbox.insert(body_listbox.size(), new_body.name)
        new_body_entry.delete(0, 'end')
    elif new_name:
        showinfo(title="Info", message="Name already in use")


def space_pressed(event):
    if root.focus_get() == space:
        if start_button["text"] == "Start":
            start_sim()
        else:
            stop_sim()


def enter_pressed(event):
    if root.focus_get() == new_body_entry:
        add_body()


def show_blocks_clicked():
    if show_blocks_button["text"] == 'Show obstacles':
        show_blocks(space)
        show_blocks_button["text"] = 'Hide obstacles'
    else:
        hide_blocks(space)
        show_blocks_button["text"] = 'Show obstacles'


def main():
    global root
    global start_button
    global space
    global body_listbox
    global new_body_entry

    global grab_button
    global grab
    global show_blocks_button
    global delete_button
    global hide_button

    global button_value

    root = tkinter.Tk()
    root.title("Soft-body")
    root.bind('<r>', lambda event: reset())


    space = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    space.bind('<Button-1>', mouse_down)
    space.bind('<Motion>', mouse_move)
    space.bind('<ButtonRelease-1>', mouse_up)

    space.pack(side=tkinter.LEFT)


    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.RIGHT)

    frame.columnconfigure(index=0, weight=2)
    frame.columnconfigure(index=1, weight=1)
    frame.rowconfigure(index=0, weight=1)
    frame.rowconfigure(index=1, weight=3)
    frame.rowconfigure(index=2, weight=1)

    start_button = tkinter.Button(frame, text="Start", command=start_sim)
    start_button.grid(row=3, column=0)
    root.bind('<space>', space_pressed)

    save_button = tkinter.Button(frame, text="Save", command=save_data)
    save_button.grid(row=3, column=1)

    reset_button = tkinter.Button(frame, text="Reset", command=reset)
    reset_button.grid(row=4, column=1)
    
    delete_button =  tkinter.Button(frame, text="Delete object", command=delete_body)
    delete_button.grid(row=2, column=1)

    hide_button = tkinter.Button(frame, text="Hide object", command=hide_body)
    hide_button.grid(row=2, column=0)

    hide_button["state"] = 'disabled'
    delete_button["state"] = 'disabled'

    new_body_entry = tkinter.Entry(frame)
    new_body_entry.grid(column=0, row=0, padx=3, pady=6, sticky=tkinter.EW)
    tkinter.Button(frame, text="Add body", command=add_body).grid(column=1, row=0, padx=6, pady=6)
    root.bind('<Return>', enter_pressed)

    body_listbox = tkinter.Listbox(frame, height=5, width=10,
                                   listvariable=tkinter.Variable(value=[x.name for x in bodies]))
    body_listbox.bind("<<ListboxSelect>>", check_selection)
    body_listbox.grid(row=1, column=0, columnspan=2, sticky=tkinter.EW, padx=5, pady=5)

    button_value = tkinter.IntVar()
    grab = tkinter.IntVar(value=0)
    grab_button = tkinter.Radiobutton(frame, text="Grab object", variable=button_value, value=1)
    grab_button.grid()

    # adding_part = tkinter.IntVar(value=0)
    add_part_button = tkinter.Radiobutton(frame, text="Add particle", variable=button_value, value=2)
    add_part_button.grid()

    # adding_con = tkinter.IntVar(value=0)
    adding_con_button = tkinter.Radiobutton(frame, text="Add connection", variable=button_value, value=3)
    adding_con_button.grid()

    show_blocks_button = tkinter.Button(frame, text="Show obstacles", command=show_blocks_clicked)
    show_blocks_button.grid()
    # reset()

    for body in bodies:
        create_body_image(space, body)

    for block in blocks:
        create_block_image(space, block)

    start_sim(init=True)

    root.mainloop()


if __name__ == '__main__':
    make_bounds()
    main()
