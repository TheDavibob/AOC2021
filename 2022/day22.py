import numpy as np
from matplotlib import pyplot as plt

import common


N_BLOCKS_WIDTH = 3
N_BLOCKS_HEIGHT = 4
BLOCK_WIDTH = 50
BLOCK_HEIGHT = 50

# For the sample
# N_BLOCKS_WIDTH = 4
# N_BLOCKS_HEIGHT = 3
# BLOCK_WIDTH = 4
# BLOCK_HEIGHT = 4


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


def step_n(current_point, delta, n, chart, part_two=False):
    for _ in range(n):
        if not part_two:
            next_point, next_delta = get_next_point(current_point, delta, chart)
        else:
            next_point, next_delta = next_step_cube(current_point, delta, chart)

        if chart[next_point] == 1:
            break

        current_point = next_point
        delta = next_delta

        chart[current_point] = 2

    return current_point, delta


LEFT_TURN = np.array([[0, 1], [-1, 0]]).T
RIGHT_TURN = LEFT_TURN.T


def turn_left(delta):
    return tuple(LEFT_TURN @ delta)


def turn_right(delta):
    return tuple(RIGHT_TURN @ delta)


def follow_instructions(instructions, chart, part_two=False):
    direction = (0, 1)

    current_point, direction = get_next_point((0, 0), direction, chart)

    for instruction in instructions:
        if instruction == "L":
            direction = turn_left(direction)
            print(f"Turned L to face {DIR_MAP[direction]}")
        elif instruction == "R":
            direction = turn_right(direction)
            print(f"Turned R to face {DIR_MAP[direction]}")
        else:
            current_point, direction = step_n(
                current_point,
                direction,
                instruction,
                chart,
                part_two=part_two
            )
            print(f"Stepped {instruction} points to {current_point}, now facing"
                  f" {DIR_MAP[direction]}")

    return current_point, direction


def get_region(current_point, chart):
    region_height = chart.shape[0] // N_BLOCKS_HEIGHT
    region_width = chart.shape[1] // N_BLOCKS_WIDTH
    row_region = current_point[0] // region_height
    col_region = current_point[1] // region_width
    return row_region + N_BLOCKS_HEIGHT*col_region


def get_point_in_region(current_point, chart):
    region_height = chart.shape[0] // N_BLOCKS_HEIGHT
    region_width = chart.shape[1] // N_BLOCKS_WIDTH
    row_region = current_point[0] % region_height
    col_region = current_point[1] % region_width
    return row_region, col_region


def get_point_from_region(point_in_region, region, chart):
    region_height = chart.shape[0] // N_BLOCKS_HEIGHT
    region_width = chart.shape[1] // N_BLOCKS_WIDTH

    row_region = region % N_BLOCKS_HEIGHT
    col_region = region // N_BLOCKS_HEIGHT

    point = (
            row_region * region_height + point_in_region[0],
            col_region * region_width + point_in_region[1]
    )

    return point


REGION_MAP = {
    4: {
        "<": (2, ">"),
        "^": (3, ">"),
    },
    8: {
        "^": (3, "^"),
        ">": (6, "<"),
        "v": (5, "<"),
    },
    5: {
        "<": (2, "v"),
        ">": (8, "^")  # This going wrong
    },
    6: {
        ">": (8, "<"),
        "v": (3, "<")
    },
    2: {
        "^": (5, ">"),
        "<": (4, ">"),
    },
    3: {
        ">": (6, "^"),
        "<": (4, "v"),
        "v": (8, "v")
    }
}

# REGION_MAP = {  # Sample text
#     6: {
#         "<": (4, "v"),
#         "^": (1, "v"),
#         ">": (11, "<"),
#     },
#     7: {
#         ">": (11, "v"),
#     },
#     8: {
#         "<": (4, "^"),
#         "v": (1, "^")
#     },
#     11: {
#         "^": (7, "<"),
#         "v": (1, ">"),
#         ">": (6, "<")
#     },
#     1: {
#         "<": (11, "^"),
#         "^": (6, "v"),
#         "v": (8, "^"),
#     },
#     4: {
#         "v": (8, ">"),
#         "^": (6, ">")
#     }
# }


DIR_MAP = {
    (0, 1): ">",
    (1, 0): "v",
    (0, -1): "<",
    (-1, 0): "^"
}

INV_DIR_MAP = {v: k for k, v in DIR_MAP.items()}


LEFT_ROTATION = {
    "^": "<",
    "<": "v",
    "v": ">",
    ">": "^"
}


RIGHT_ROTATION = {v: k for k, v in LEFT_ROTATION.items()}


FLIP = {
    "^": "v",
    "v": "^",
    "<": ">",
    ">": "<"
}


def next_step_cube(current_point, delta, chart):
    next_point = (
        (current_point[0] + delta[0]),
        (current_point[1] + delta[1]),
    )

    out_of_bounds = False
    if (next_point[0] < 0) or (next_point[0] >= chart.shape[0]):
        out_of_bounds = True
    if (next_point[1] < 0) or (next_point[1] >= chart.shape[1]):
        out_of_bounds = True

    if (not out_of_bounds) and (chart[next_point] != -1):
        return next_point, delta

    current_region = get_region(current_point, chart)
    direction_as_char = DIR_MAP[delta]

    new_region, new_direction = REGION_MAP[current_region][direction_as_char]

    next_point_in_region = get_point_in_region(next_point, chart)

    if new_direction == direction_as_char:
        point_in_new_region = next_point_in_region
        new_delta = delta
    elif new_direction == LEFT_ROTATION[direction_as_char]:
        point_in_new_region = turn_left(next_point_in_region)
        point_in_new_region = (
            point_in_new_region[0] % (BLOCK_HEIGHT-1),
            point_in_new_region[1] % (BLOCK_WIDTH-1)
        )
        new_delta = turn_left(delta)
    elif new_direction == RIGHT_ROTATION[direction_as_char]:
        point_in_new_region = turn_right(next_point_in_region)
        point_in_new_region = (
            point_in_new_region[0] % (BLOCK_HEIGHT-1),
            point_in_new_region[1] % (BLOCK_WIDTH-1)
        )
        new_delta = turn_right(delta)
    elif new_direction == FLIP[direction_as_char]:
        point_in_new_region = (
            BLOCK_HEIGHT - 1 - next_point_in_region[0],
            BLOCK_WIDTH - 1 - next_point_in_region[1]
        )
        new_delta = (-delta[0], -delta[1])
    else:
        raise ValueError("Direction mismatch")

    if new_delta == (1, 0):
        point_in_new_region = (0, point_in_new_region[1])
    elif new_delta == (0, 1):
        point_in_new_region = (point_in_new_region[0], 0)
    elif new_delta == (-1, 0):
        point_in_new_region = (BLOCK_HEIGHT-1, point_in_new_region[1])
    elif new_delta == (0, -1):
        point_in_new_region = (point_in_new_region[0], BLOCK_WIDTH-1)


    new_point = get_point_from_region(point_in_new_region, new_region, chart)
    print(f"Proposed point: {new_point}")
    return new_point, new_delta



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

    # final_loc, final_dir = follow_instructions(instructions, chart)
    #
    # common.part(1, 1000*(final_loc[0]+1) + 4*(final_loc[1]+1) + VALUE[final_dir])

    final_loc, final_dir = follow_instructions(
        instructions,
        chart,
        part_two=True
    )

    common.part(2, 1000*(final_loc[0]+1) + 4*(final_loc[1]+1) + VALUE[final_dir])

    plt.matshow(chart)
    plt.show()