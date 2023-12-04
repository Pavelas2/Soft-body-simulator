import tkinter
from save import *
from visual import *
from physic import *
from objects import *
import itertools as it

simulation_started = True

bodies = []

parts1 = [Particle(300, 300, 5, color="blue", Vx=-0),
          Particle(400, 300, 5, color="red"),
          Particle(400, 400, 5, color="yellow"),
          Particle(300, 400, 5, color="brown"),
          Particle(350, 350, 5, Vy=0.0)]

parts = [Particle(300, 550, 5, color="blue", Vx=0),
         Particle(400, 550, 5, color="red"),
         Particle(350, 450, 5, Vy=0.0),
         Particle(350, 510, 5, Vy=-0)]

'''connects1 = [Connection((parts[0], parts[1])),
            Connection((parts[0], parts[3])),
            Connection((parts[0], parts[4])),
            Connection((parts[1], parts[4])),
            Connection((parts[1], parts[2])),
            Connection((parts[2], parts[3])),
            Connection((parts[2], parts[4])),
            Connection((parts[3], parts[4]))]'''

connects = [Connection((parts[0], parts[1])),
            Connection((parts[0], parts[2])),
            Connection((parts[1], parts[2])),
            Connection((parts[3], parts[0])),
            Connection((parts[3], parts[1])),
            Connection((parts[3], parts[2]))]

bodies.append(Body(connects=connects, parts=parts))


def start_sim():
    global simulation_started
    simulation_started = True

    start_button["text"] = "Stop"
    start_button["command"] = stop_sim

    for body in bodies:
        create_image(space, body)

    simulation()


def stop_sim():
    global simulation_started
    simulation_started = False

    start_button["text"] = "Start"
    start_button["command"] = start_sim


def simulation():
    for body in bodies:
        body.update_pos()
        update_image(space, body)

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
