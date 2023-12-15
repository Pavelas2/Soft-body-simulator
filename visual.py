def create_body_image(space, body):
    """Создаёт изображения для частиц и связей тела"""
    for connect in body.connects:
        create_connection_image(space, connect)
    for part in body.parts:
        create_part_image(space, part)

def create_connection_image(space, connect):
    """Создаёт изображение для связи"""
    if not connect.image:
        connect.image = space.create_line(*connect.parts[0].pos, *connect.parts[1].pos, fill='black')


def create_part_image(space, part):
    """Создаёт изображение для частицы"""
    if not part.image:
        x = part.pos[0]
        y = part.pos[1]
        r = part.r
        part.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=part.color)


def update_body_image(space, body):
    """Обновляет изображение тела"""
    for connect in body.connects:
        space.coords(connect.image, *connect.parts[0].pos, *connect.parts[1].pos)
    for part in body.parts:
        space.itemconfig(part.image, fill="red" if body.chosen else "black")
        x = part.pos[0]
        y = part.pos[1]
        r = part.r
        space.coords(part.image, x - r, y - r, x + r, y + r)


def delete(space, bodies):
    """Удаляет изображения частиц и связей тела"""
    for body in bodies:
        for connect in body.connects:
            space.delete(connect.image)
        for part in body.parts:
            space.delete(part.image)


def create_block_image(space, block):
    """Создаёт изображение препядствия"""
    block.image = space.create_polygon(*block.points, fill="black")

def delete_block_image(space, block):
    space.delete(block.image)
