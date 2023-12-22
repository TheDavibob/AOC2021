import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import convolve2d

import common


KERNEL = np.array([
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0]
])


def parse_input(text):
    return common.convert_string_to_np_array(text, {".": 0, "#": 1, "S": 2}).astype(int)


def step(position_grid, wall_grid):
    new_positions = convolve2d(position_grid, KERNEL, mode="same")

    return (new_positions > 0) & ~wall_grid


def part_one(input_grid, n_steps=64):
    positions = (input_grid == 2)
    wall_grid = (input_grid == 1)

    for _ in range(n_steps):
        positions = step(positions, wall_grid)

    return np.sum(positions)



def part_two_again(input_grid, N):

    full_cycles = N // 131
    complete_cells_in_row = full_cycles - 1
    n_same_parity_in_row = (complete_cells_in_row+1) // 2

    n_same_parity_total = n_same_parity_in_row ** 2
    n_complete_total = complete_cells_in_row * (complete_cells_in_row + 1) // 2
    n_alt_parity_total = n_complete_total - n_same_parity_total

    mostly_complete_remainder = 131 + (N % 131)
    mostly_incomplete_remainder = (N % 131)

    total_mostly_complete = full_cycles
    total_mostly_incomplete = full_cycles + 1

    bottom_right = np.vstack((input_grid[65:], input_grid[:65]))
    bottom_right = np.hstack((
        bottom_right[:, 65:],
        bottom_right[:, :65])
    )

    bottom_left = np.vstack((input_grid[65:], input_grid[:65]))
    bottom_left = np.hstack((
        bottom_left[:, 66:],
        bottom_left[:, :66])
    )
    bottom_left = bottom_left[:, ::-1]

    upper_left = np.vstack((input_grid[66:], input_grid[:66]))
    upper_left = np.hstack((
        upper_left[:, 66:],
        upper_left[:, :66])
    )
    upper_left = upper_left[::-1, ::-1]

    upper_right = np.vstack((input_grid[66:], input_grid[:66]))
    upper_right = np.hstack((
        upper_right[:, 65:],
        upper_right[:, :65])
    )
    upper_right = upper_right[::-1, :]

    each_grid = (
        bottom_right,
        bottom_left,
        upper_left,
        upper_right
    )

    total = 0
    for corner in each_grid:
        fourfold = np.tile(corner==1, (2, 2)).astype(int)
        fourfold[(0, 0)] = 2

        positions = (fourfold == 2)
        wall_grid = (fourfold == 1)
        n_at = []
        for _ in range(263):
            n_at.append(np.sum((positions == 1)[:131, :131]))
            positions = step(positions, wall_grid)

        if N % 2 == 0:
            same_parity = n_at[-1]
            alt_parity = n_at[-2]
        else:
            same_parity = n_at[-2]
            alt_parity = n_at[-1]

        total += (
                same_parity * n_same_parity_total
                + alt_parity * n_alt_parity_total
                + total_mostly_complete * n_at[mostly_complete_remainder]
                + total_mostly_incomplete * n_at[mostly_incomplete_remainder]
        )

    # Double counted centre line
    total -= (N + 1) * 4
    if (N % 2) == 1:
        total += 2 * (N+1)
    else:
        total += 2*N + 1

    return total


if __name__ == "__main__":
    input_grid = parse_input(common.import_file("input/day21"))

    common.part(1, part_one(input_grid, n_steps=64))

    common.part(2, part_two_again(input_grid, 26501365))

    # Below: demo that part 2 works.
    # twentyfivefold = np.tile(input_grid == 1, (5, 5)).astype(int)
    # twentyfivefold[2*131+65, 2*131+65] = 2
    #
    # positions = (twentyfivefold == 2)
    # wall_grid = (twentyfivefold == 1)
    #
    # for N in range(120):
    #     positions = step(positions, wall_grid)
    #
    # for N in range(120, 300):
    #     print(N, np.sum(positions==1), part_two_again(input_grid, N))
    #     positions = step(positions, wall_grid)
