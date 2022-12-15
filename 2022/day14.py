import numpy as np
from matplotlib import pyplot as plt

import common


def parse_input(text, part_two=False):
    chains = []
    max_x = None
    min_x = None
    max_y = None
    min_y = 1

    for line in text.split("\n"):
        if line == "":
            continue

        chain = []
        for point in line.split(" -> "):
            x, y = point.split(",")
            chain.append((int(x), int(y)))
            if (max_x is None) or (int(x) > max_x):
                max_x = int(x)

            if (min_x is None) or (int(x) < min_x):
                min_x = int(x)

            if (max_y is None) or (int(y) > max_y):
                max_y = int(y)

            if (min_y is None) or (int(y) < min_y):
                min_y = int(y)

        chains.append(chain)

    if part_two:
        max_y += 1
        max_x += max_y
        min_x -= max_y

    grid_width = max_x - min_x + 3
    grid_height = max_y - min_y + 3

    def point_in_grid(x, y):
        return x - min_x + 1, y - min_y + 1

    # grid_width = max_x + 1
    # grid_height = max_y + 1
    # def point_in_grid(x, y):
    #     return x, y

    array = np.zeros((grid_width, grid_height), dtype=int)
    for chain in chains:
        for point_before, point_after in zip(chain[:-1], chain[1:]):
            offset_before = point_in_grid(*point_before)
            offset_after = point_in_grid(*point_after)

            unit_x = int(np.sign(offset_after[0] - offset_before[0]))
            unit_y = int(np.sign(offset_after[1] - offset_before[1]))

            point = offset_before
            while point != offset_after:
                array[point] = 1
                point = (point[0] + unit_x, point[1] + unit_y)

            array[point] = 1

    if part_two:
        array[:, -1] = 1

    return array, point_in_grid


def step_sand(array, start_point):
    point = start_point
    if array[start_point] != 0:
        return array, False

    while True:
        next_line = point[1] + 1
        if next_line >= array.shape[1]:
            return array, False  # sand fallen through

        if array[point[0], next_line] == 0:
            point = (point[0], next_line)
        elif array[point[0]-1, next_line] == 0:
            point = (point[0]-1, next_line)
        elif array[point[0]+1, next_line] == 0:
            point = (point[0]+1, next_line)
        else:
            array[point] = 2
            break

    return array, True



if __name__ == "__main__":
    text = common.load_todays_input(__file__)
#     text = """
# 498,4 -> 498,6 -> 496,6
# 503,4 -> 502,4 -> 502,9 -> 494,9
# """
    array, point_in_grid = parse_input(text)

    start_point = point_in_grid(500, 0)
    success = True
    counter = 0
    while success:
        array, success = step_sand(array, start_point)
        counter += 1

    common.part(1, counter-1)

    array_2, point_in_grid = parse_input(text, part_two=True)
    start_point = point_in_grid(500, 0)
    success = True
    counter = 0
    while success:
        array_2, success = step_sand(array_2, start_point)
        counter += 1

    common.part(2, counter-1)

    plt.matshow(array_2.T)
