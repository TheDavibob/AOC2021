import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

import common


def parse_input(text):
    map_block, instructions_block = text.split("\n\n")
    map = common.convert_string_to_np_array(map_block, {".": 0, "#": 1, "O": 2, "@": 3})

    instructions = "".join(instructions_block.split("\n"))

    return map, instructions


def step(map, instruction):
    if instruction == "^":
        direction = (-1, 0)
    elif instruction == ">":
        direction = (0, 1)
    elif instruction == "<":
        direction = (0, -1)
    elif instruction == "v":
        direction = (1, 0)
    else:
        raise ValueError(f"Direction {instruction} not understood")

    current_loc = tuple(x[0] for x in np.where(map == 3))
    next_loc = current_loc
    n_steps = 1
    while True:
        next_loc = (next_loc[0] + direction[0], next_loc[1] + direction[1])
        if map[next_loc] == 1:
            can_move = False
            break
        elif map[next_loc] == 0:
            can_move = True
            break

        n_steps += 1

    new_map = map.copy()
    if not can_move:
        return new_map
    if n_steps == 1:
        new_map[current_loc] = 0
        new_map[next_loc] = 3
    else:
        new_map[current_loc] = 0
        new_map[next_loc] = 2
        new_map[current_loc[0] + direction[0], current_loc[1] + direction[1]] = 3

    return new_map


def step_wide(map, instruction):
    if instruction == "^":
        direction = (-1, 0)
    elif instruction == ">":
        direction = (0, 1)
    elif instruction == "<":
        direction = (0, -1)
    elif instruction == "v":
        direction = (1, 0)
    else:
        raise ValueError(f"Direction {instruction} not understood")

    current_loc = tuple(x[0] for x in np.where(map == 3))
    movement_map = {}

    points_to_check = [current_loc]
    while len(points_to_check) > 0:
        new_points_to_check = []
        for point in points_to_check:
            value = map[point]
            new_location = (point[0] + direction[0], point[1] + direction[1])
            new_value = map[new_location]
            if new_value == 0:
                # Can move it
                pass
            elif new_value == 1:
                # Can not move it
                return map.copy()
            elif new_value == 4:
                new_points_to_check.append(new_location)
                if instruction in ("^", "v"):
                    new_points_to_check.append((new_location[0], new_location[1] + 1))
            elif new_value == 5:
                new_points_to_check.append(new_location)
                if instruction in ("^", "v"):
                    new_points_to_check.append((new_location[0], new_location[1] - 1))

            movement_map[point] = (value, new_location)
            points_to_check = new_points_to_check

    new_map = map.copy()
    for old_loc in movement_map.keys():
        new_map[old_loc] = 0
    for value, new_loc in movement_map.values():
        new_map[new_loc] = value

    return new_map

def get_score(map, target_val=2):
    score = 0
    for b0, b1 in zip(*np.where(map == target_val)):
        print(b0, b1)
        score += 100*b0 + b1
    return score


def widen_map(map):
    wide_map = np.zeros((map.shape[0], 2*map.shape[1]), dtype=int)
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i, j] == 1:
                wide_map[i, 2*j] = 1
                wide_map[i, 2*j + 1] = 1
            elif map[i, j] == 2:
                wide_map[i, 2*j] = 4  # left box
                wide_map[i, 2*j+1] = 5  # right box
            elif map[i, j] == 3:
                wide_map[i, 2*j] = 3

    return wide_map


if __name__ == "__main__":
    with open("input/day15") as file:
        text = file.read()

#     text = """########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########
#
# <^^>>>vv<v>>v<<"""

    map, instructions = parse_input(text)

    current_map = map.copy()
    maps = [current_map]
    for instruction in tqdm(instructions):
        current_map = step(current_map, instruction)
        maps.append(current_map)

    # 1462552 is too low
    print(f"Part 1: {get_score(current_map)}")

    wide_map = widen_map(map)
    # plt.imshow(wide_map)

    current_map = wide_map.copy()
    maps = [current_map]
    for instruction in tqdm(instructions):
        current_map = step_wide(current_map, instruction)
        maps.append(current_map)

    # 1462552 is too low
    print(f"Part 2: {get_score(current_map, target_val=4)}")