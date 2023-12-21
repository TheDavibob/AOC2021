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

    plt.matshow(positions)
    plt.show()

    return np.sum(positions)


def part_two(input_grid):
    reps = 4
    part_two_grid = np.tile(input_grid == 1, (2*reps+1, 2*reps+1)).astype(int)
    part_two_grid[65 + reps * input_grid.shape[0], 65 + reps * input_grid.shape[1]] = 2

    positions = (part_two_grid == 2)
    wall_grid = (part_two_grid == 1)

    positions_at_steps = []
    for _ in range(part_two_grid.shape[0] // 2):
        positions = step(positions, wall_grid)
        positions_at_steps.append(np.sum(positions))
    return positions_at_steps



if __name__ == "__main__":
    input_grid = parse_input(common.import_file("input/day21"))

    common.part(1, part_one(input_grid))

    positions_at_steps = part_two(input_grid)

    demo_grid = parse_input("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""")
    print(part_one(demo_grid, 32))
    print(part_one(demo_grid, 33))

    # Notes:
    # Covered squares is approximately:
    #   2*(n_steps - half_width) // width horizontally
    #   2*(n_steps - half_height) // height vertically
    #   0.5 * ((n_steps - half_width) // width - 1) * ((n_steps - half_height) //
    #   height - 1) in each diagonal, of which there are four.
    # These probably alternate odd/even
    # For demo, we have:
    # weight = (steps - 5) // 11
    # (4*weight + 2*(weight-1)**2 ) * ((42 + 39)/2) is a good proxy
    # (Even cells 42, odd cells 39)

    # There should therefore be some sort of periodicity, but with this strange
    # scaling