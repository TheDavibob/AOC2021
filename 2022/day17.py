import warnings

import numpy as np
from tqdm import tqdm

import common


def manifest_next_rock(idx, big_grid):
    first_row = big_grid.shape[0]
    for i in range(big_grid.shape[0], 0, -1):
        if np.any(big_grid[i-1]):
            first_row = i
            break

    rock_idx = idx % 5
    if rock_idx == 0:
        rock = np.ones((1, 4), dtype=int)
    elif rock_idx == 1:
        rock = np.ones((3, 3), dtype=int)
        for a in (0, -1):
            for b in (0, -1):
                rock[a, b] = 0
    elif rock_idx == 2:
        rock = np.ones((3, 3), dtype=int)
        rock[1:, :2] = 0  # upside down
    elif rock_idx == 3:
        rock = np.ones((4, 1), dtype=int)
    elif rock_idx == 4:
        rock = np.ones((2, 2), dtype=int)
    else:
        raise ValueError("Unexpected rock type")

    new_shape = (first_row + 3 + rock.shape[0], big_grid.shape[1])
    new_big_grid = np.zeros(new_shape, dtype=int)
    new_big_grid[:first_row] = big_grid[:first_row]

    rock_bottom_left = (first_row + 3, 2)

    return new_big_grid, rock, rock_bottom_left


def step(big_grid, instruction, rock, rock_bottom_left):
    can_fall = False
    if instruction == ">":
        if can_rock_fit(big_grid, rock, (rock_bottom_left[0], rock_bottom_left[1] + 1)):
            new_bl = (rock_bottom_left[0], rock_bottom_left[1] + 1)
        else:
            new_bl = rock_bottom_left
    elif instruction == "<":
        if can_rock_fit(big_grid, rock, (rock_bottom_left[0], rock_bottom_left[1] - 1)):
            new_bl = (rock_bottom_left[0], rock_bottom_left[1] - 1)
        else:
            new_bl = rock_bottom_left
    else:
        warnings.warn(f"Unexpected instruction {instruction}")
        return rock_bottom_left, can_fall

    if can_rock_fit(big_grid, rock, (new_bl[0]-1, new_bl[1])):
        new_bl = (new_bl[0]-1, new_bl[1])
        can_fall = True

    return new_bl, can_fall


def can_rock_fit(big_grid, rock, rock_bottom_left):
    if rock_bottom_left[1] < 0:
        return False
    elif rock_bottom_left[0] < 0:
        return False
    elif rock_bottom_left[1]+rock.shape[1] > big_grid.shape[1]:
        return False
    rock_on_grid = vis_rock_on_grid(big_grid, rock, rock_bottom_left)

    return not np.any(rock_on_grid & big_grid)


def vis_rock_on_grid(big_grid, rock, rock_bottom_left):

    rock_on_grid = np.zeros_like(big_grid)

    rock_on_grid[
        rock_bottom_left[0]:rock_bottom_left[0]+rock.shape[0],
        rock_bottom_left[1]:rock_bottom_left[1]+rock.shape[1]
    ] = rock
    return rock_on_grid


def step_rock(big_grid, idx, instructions, instructions_idx):
    big_grid, rock, rock_bl = manifest_next_rock(idx, big_grid)
    can_fall = True
    while can_fall:
        # print((big_grid + 2*vis_rock_on_grid(big_grid, rock, rock_bl))[::-1])
        next_instruction = instructions[instructions_idx]
        rock_bl, can_fall = step(big_grid, next_instruction, rock, rock_bl)
        instructions_idx += 1
        instructions_idx %= len(instructions)

    big_grid = big_grid + vis_rock_on_grid(big_grid, rock, rock_bl)

    return big_grid, instructions_idx


def cycle(n, instructions):
    big_grid = np.zeros((0, 7))
    instructions_idx = 0
    for idx in tqdm(range(n)):
        big_grid, instructions_idx = step_rock(big_grid, idx, instructions, instructions_idx)

    # print(big_grid[::-1])
    return big_grid


def get_grid_height(grid):
    i=1
    for i in range(1, grid.shape[0]):
        if np.any(grid[-i:]):
            break

    empty_lines = i-1
    height = grid.shape[0] - empty_lines
    return height



if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    # instructions = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    instructions = text.split("\n")[0]
    big_grid = cycle(2022, instructions)

    common.part(1, get_grid_height(big_grid))

    # big_grid = cycle(1000000000000, instructions)
    common.part(2, get_grid_height(big_grid))
