window_width = 600
window_height = 600


def create_body_image(space, body):
    for connect in body.connects:
        if not connect.image:
            connect.image = space.create_line(*connect.parts[0].pos, *connect.parts[1].pos, fill='black')
        for part in connect.parts:
            if not part.image:
                x = part.pos[0]
                y = part.pos[1]
                r = part.r
                part.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=part.color)


def update_body_image(space, body):
    for connect in body.connects:
        space.coords(connect.image, *connect.parts[0].pos, *connect.parts[1].pos)
        for part in connect.parts:
            x = part.pos[0]
            y = part.pos[1]
            r = part.r
            space.coords(part.image, x - r, y - r, x + r, y + r)


def create_block_image(space, block):
    block.image = space.create_line(*block.points)
