import numpy as np
from matplotlib import pyplot as plt


def parse_input(text):
    things = []
    for line in text.split("\n"):
        if line == "":
            continue

        p, v = line.split(" ")
        _, xy = p.split("=")
        x, y = xy.split(",")

        _, uw = v.split("=")
        u, w = uw.split(",")

        things.append(
            (
                (int(x), int(y)),
                (int(u), int(w)),
            )
        )

    return things


def pos_after_n(
        pos: int,
        vel: int,
        shape: int,
        n: int
):
    return (pos + (vel * n)) % shape


def quadrant_after_n(
        pos,
        vel,
        shape,
        n
):
    x = pos_after_n(pos[0], vel[0], shape[0], n)
    y = pos_after_n(pos[1], vel[1], shape[1], n)

    quadrant_bdy_x = (shape[0]-1) // 2
    quadrant_bdy_y = (shape[1]-1) // 2

    if x < quadrant_bdy_x:
        if y < quadrant_bdy_y:
            return 0  # 00
        elif y > quadrant_bdy_y:
            return 1  # 01
    elif x > quadrant_bdy_x:
        if y < quadrant_bdy_y:
            return 2  # 10
        elif y > quadrant_bdy_y:
            return 3  # 11

    return None


def all_positions_after_n(things, shape, n):
    xs = []
    ys = []
    for pos, vel in things:
        x = pos_after_n(pos[0], vel[0], shape[0], n)
        y = pos_after_n(pos[1], vel[1], shape[1], n)
        xs.append(x)
        ys.append(y)

    return xs, ys


def part_one(
        things,
        n,
        shape
):
    quads = {x: 0 for x in range(4)}

    for xy, uv in things:
        q = quadrant_after_n(xy, uv, shape, n)
        if q is not None:
            quads[q] += 1
    return quads


if __name__ == "__main__":
    with open("input/day14") as file:
        text = file.read()

    N = 100
    SHAPE = (101, 103)
    things = parse_input(text)
    quads = part_one(things, N, SHAPE)

    # 362 is too low
    print(quads[0] * quads[1] * quads[2] * quads[3])

    # for n in range(10000):
    #     print(n)
    #     quads = part_one(things, n, SHAPE)
    #     xs, ys = all_positions_after_n(things, SHAPE, n)
    #     grid = np.zeros(SHAPE, dtype=bool)
    #     for x, y in zip(xs, ys):
    #         grid[x, y] = True
    #
    #     plt.matshow(grid.T)
    #     plt.savefig(f"{n}.png")

    hor_offset = 14  # + 101
    ver_offset = 94  # + 103
    # N = 14 + a * 101 = 94 + b * 103
    # Find N such that N - 14 is a multiple of 101 and N - 94 is a multiple of 103
    for n in range(101 * 103):
        if (n - 14) % 101 != 0:
            continue

        if (n - 94) % 103 != 0:
            continue

        print(n)
        break

    xs, ys = all_positions_after_n(things, SHAPE, n)
    grid = np.zeros(SHAPE, dtype=bool)
    for x, y in zip(xs, ys):
        grid[x, y] = True

    plt.matshow(grid.T)
    plt.savefig(f"tree.png")