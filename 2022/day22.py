import numpy as np
from matplotlib import pyplot as plt

import common


def parse_input(text):
    map_text, instructions = text.split("\n\n")
    map_height = len(map_text.split("\n"))
    map_width = max([len(line) for line in map_text.split("\n")])

    mapping = {
        " ": -1,
        ".": 0,
        "#": 1,
    }

    chart = -np.ones((map_height, map_width), dtype=int)
    for i, line in enumerate(map_text.split("\n")):
        for j, char in enumerate(line):
            chart[i, j] = mapping[char]

    instructions = instructions.split("\n")[0]

    current_set = ""
    instruction_set = []
    for char in instructions:
        if char in ["L", "R"]:
            instruction_set.append(int(current_set))
            current_set = ""
            instruction_set.append(char)
        else:
            current_set += char

    if current_set != "":
        instruction_set.append(int(current_set))

    return chart, instruction_set


def get_next_point(current_point, delta, chart):
    next_point = (
        (current_point[0] + delta[0]) % chart.shape[0],
        (current_point[1] + delta[1]) % chart.shape[1],
    )

    while chart[next_point] == -1:
        next_point = (
            (next_point[0] + delta[0]) % chart.shape[0],
            (next_point[1] + delta[1]) % chart.shape[1],
        )

    return next_point, delta


def step_n(current_point, delta, n, chart):
    for _ in range(n):
        next_point, delta = get_next_point(current_point, delta, chart)
        if chart[next_point] == 1:
            break

        current_point = next_point

    return current_point, delta


LEFT_TURN = np.array([[0, 1], [-1, 0]]).T
RIGHT_TURN = LEFT_TURN.T


def turn_left(delta):
    return tuple(LEFT_TURN @ delta)


def turn_right(delta):
    return tuple(RIGHT_TURN @ delta)

def follow_instructions(instructions, chart):
    direction = (0, 1)

    current_point, direction = get_next_point((0, 0), direction, chart)

    for instruction in instructions:
        if instruction == "L":
            direction = turn_left(direction)
        elif instruction == "R":
            direction = turn_right(direction)
        else:
            current_point, direction = step_n(current_point, direction, instruction, chart)

    return current_point, direction


def next_step_cube(current_point, delta, chart):
    ...


VALUE = {
    (0, 1): 0,
    (1, 0): 1,
    (0, -1): 2,
    (-1, 0): 3
}


test_input = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    chart, instructions = parse_input(text)

    # plt.matshow(chart)
    # plt.show()

    final_loc, final_dir = follow_instructions(instructions, chart)

    common.part(1, 1000*(final_loc[0]+1) + 4*(final_loc[1]+1) + VALUE[final_dir])

    common.part(2, "TBC")
