window_width = 600
window_height = 600


def create_image(space, body):
    for connect in body.connects:
        if not connect.image:
            connect.image = space.create_line(connect.parts[0].x, connect.parts[0].y, connect.parts[1].x,
                                              connect.parts[1].y)
        for part in connect.parts:
            if not part.image:
                x = part.x
                y = part.y
                r = part.r
                part.image = space.create_oval([x - r, part.y - r], [x + r, y + r], fill=part.color)


def update_image(space, body):
    for connect in body.connects:
        space.coords(connect.image, connect.parts[0].x, connect.parts[0].y, connect.parts[1].x, connect.parts[1].y)
        for part in connect.parts:
            x = part.x
            y = part.y
            r = part.r
            space.coords(part.image, x - r, y - r, x + r, y + r)
