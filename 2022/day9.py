import warnings

import numpy as np
import common


def parse_input(text):
    instructions = []

    for line in text.split("\n"):
        if line == "":
            continue

        direction, dist = line.split(" ")
        instructions.append((direction, int(dist)))

    return instructions


def new_tail_pos(prev_tail_pos, head_pos):
    if (
            (abs(prev_tail_pos[0] - head_pos[0]) == 1)
            and (abs(prev_tail_pos[1] - head_pos[1]) == 1)
    ):
        new_x = prev_tail_pos[0]
        new_y = prev_tail_pos[1]
    elif(
            (abs(prev_tail_pos[0] - head_pos[0]) == 2)
            and (abs(prev_tail_pos[1] - head_pos[1]) == 2)
    ):
        if prev_tail_pos[0] - head_pos[0] == 2:
            new_x = prev_tail_pos[0] - 1
        elif prev_tail_pos[0] - head_pos[0] == -2:
            new_x = prev_tail_pos[0] + 1

        if prev_tail_pos[1] - head_pos[1] == 2:
            new_y = prev_tail_pos[1] - 1
        elif prev_tail_pos[1] - head_pos[1] == -2:
            new_y = prev_tail_pos[1] + 1
    elif (
            (abs(prev_tail_pos[0] - head_pos[0]) == 1)
            and (abs(prev_tail_pos[1] - head_pos[1]) == 2)
    ):
        new_x = head_pos[0]
        if prev_tail_pos[1] - head_pos[1] == 2:
            new_y = prev_tail_pos[1] - 1
        elif prev_tail_pos[1] - head_pos[1] == -2:
            new_y = prev_tail_pos[1] + 1
    elif (
            (abs(prev_tail_pos[0] - head_pos[0]) == 2)
            and (abs(prev_tail_pos[1] - head_pos[1]) == 1)
    ):
        new_y = head_pos[1]
        if prev_tail_pos[0] - head_pos[0] == 2:
            new_x = prev_tail_pos[0] - 1
        elif prev_tail_pos[0] - head_pos[0] == -2:
            new_x = prev_tail_pos[0] + 1
    elif abs(prev_tail_pos[0] - head_pos[0]) == 2:
        new_y = prev_tail_pos[1]
        if prev_tail_pos[0] - head_pos[0] == 2:
            new_x = prev_tail_pos[0] - 1
        elif prev_tail_pos[0] - head_pos[0] == -2:
            new_x = prev_tail_pos[0] + 1
    elif abs(prev_tail_pos[1] - head_pos[1]) == 2:
        new_x = prev_tail_pos[0]
        if prev_tail_pos[1] - head_pos[1] == 2:
            new_y = prev_tail_pos[1] - 1
        elif prev_tail_pos[1] - head_pos[1] == -2:
            new_y = prev_tail_pos[1] + 1
    else:
        new_x, new_y = prev_tail_pos

    tail_pos = (new_x, new_y)
    return tail_pos


def step(direction, prev_head_pos, prev_tail_pos):
    head_pos = move_head(direction, prev_head_pos)

    tail_pos = new_tail_pos(prev_tail_pos, head_pos)

    return head_pos, tail_pos


def move_head(direction, prev_head_pos):
    if direction == "L":
        head_pos = (prev_head_pos[0] - 1, prev_head_pos[1])
    elif direction == "R":
        head_pos = (prev_head_pos[0] + 1, prev_head_pos[1])
    elif direction == "U":
        head_pos = (prev_head_pos[0], prev_head_pos[1] + 1)
    elif direction == "D":
        head_pos = (prev_head_pos[0], prev_head_pos[1] - 1)
    else:
        raise ValueError("Direction not understood")
    return head_pos


def step_big(direction, prev_head_pos, prev_tail_poses):
    head_pos = move_head(direction, prev_head_pos)
    tail_poses = []
    tail_poses.append(new_tail_pos(prev_tail_poses[0], head_pos))
    for i in range(1, len(prev_tail_poses)):
        tail_poses.append(new_tail_pos(prev_tail_poses[i], tail_poses[-1]))

    return head_pos, tail_poses


test_input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""


test_input_2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""


if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    instructions = parse_input(text)

    # instructions = parse_input(test_input)

    head_pos = (0, 0)
    tail_pos = (0, 0)
    all_tail_pos = {tail_pos}
    for instruction in instructions:
        direction, dist = instruction
        for _ in range(dist):
            head_pos, tail_pos = step(direction, head_pos, tail_pos)
            if tail_pos not in all_tail_pos:
                all_tail_pos.add(tail_pos)

    common.part(1, len(all_tail_pos))

    # instructions = parse_input(test_input)
    # instructions = parse_input(test_input_2)

    head_pos = (0, 0)
    tail_poses = [(0, 0) for _ in range(9)]
    all_tail_pos = [tail_poses[-1]]
    for instruction in instructions:
        direction, dist = instruction
        for _ in range(dist):
            head_pos, tail_poses = step_big(direction, head_pos, tail_poses)
            if tail_poses[-1] not in all_tail_pos:
                all_tail_pos.append(tail_poses[-1])

    common.part(2, len(all_tail_pos))
