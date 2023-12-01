import tkinter

window_width = 600
window_height = 600


def main():
    root = tkinter.Tk()
    # пространство отображается на холсте типа Canvas
    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="white")
    space.pack(side=tkinter.TOP)
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.RIGHT)

    root.mainloop()


if __name__ == '__main__':
    main()
