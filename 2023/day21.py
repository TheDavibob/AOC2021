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

    # plt.matshow(positions)
    # plt.show()

    return np.sum(positions)


def part_two(input_grid):
    reps = 4
    part_two_grid = np.tile(input_grid == 1, (2*reps+1, 2*reps+1)).astype(int)
    part_two_grid[65 + reps * input_grid.shape[0], 65 + reps * input_grid.shape[1]] = 2

    positions = (part_two_grid == 2)
    wall_grid = (part_two_grid == 1)

    positions_at_steps = []
    positions_at_steps.append(1)
    for _ in range(part_two_grid.shape[0] // 2):
        positions = step(positions, wall_grid)
        positions_at_steps.append(np.sum(positions))
    return positions_at_steps


def step_input_grid_from_cell(grid, cell):
    wall_grid = (grid == 1)

    positions = np.zeros_like(wall_grid)
    positions[cell] = 2

    positions_at_steps = []

    for i in range(sum(grid.shape)+2):
        positions = step(positions, wall_grid)
        positions_at_steps.append(np.sum(positions))

    return positions_at_steps


if __name__ == "__main__":
    input_grid = parse_input(common.import_file("input/day21"))

    common.part(1, part_one(input_grid))

    # positions_at_steps = part_two(input_grid)

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
    # print(part_one(demo_grid, 32))
    # print(part_one(demo_grid, 33))

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

    # input_grid = demo_grid

    upper_left = step_input_grid_from_cell(input_grid, (0, 0))
    upper_right = step_input_grid_from_cell(input_grid, (0, -1))
    lower_left = step_input_grid_from_cell(input_grid, (-1, 0))
    lower_right = step_input_grid_from_cell(input_grid, (-1, -1))

    centre_point = input_grid.shape[0] // 2

    centre_left = step_input_grid_from_cell(input_grid, (centre_point, 0))
    centre_right = step_input_grid_from_cell(input_grid, (centre_point, -1))
    centre_up = step_input_grid_from_cell(input_grid, (-1, centre_point))
    centre_down = step_input_grid_from_cell(input_grid, (0, centre_point))

    centre = step_input_grid_from_cell(input_grid, (centre_point, centre_point))

    known_values = part_two(input_grid)

    # The following works for N up to around 190 but not 200.
    print(known_values[210])

    N = 210
    line_blocks = (N - centre_point) // input_grid.shape[0]
    rem = (N-centre_point) % input_grid.shape[0] - 2

    score = 0
    if N % 2 == 0:
        odd_blocks = line_blocks // 2
        even_blocks = line_blocks - odd_blocks

    else:
        even_blocks = line_blocks // 2
        odd_blocks = line_blocks - even_blocks

    # NO: Next one started doesn't mean this one is finished
    score += 4 * centre_left[-1] * even_blocks + 4 * centre_left[-2] * odd_blocks

    score += centre_left[rem] + centre_down[rem] + centre_up[rem] + centre_right[rem]

    if N % 2 == 0:
        score += centre[-1]
    else:
        score += centre[-2]

    completed_diag_block_line = (N - 2*centre_point) // input_grid.shape[0]
    rem_diag_blocks = (N - 2*centre_point) % input_grid.shape[0] - 3

    if completed_diag_block_line < 0:
        completed_diag_block_line = 0
        rem_diag_blocks = 0

    total_completed_diag_blocks = completed_diag_block_line * (completed_diag_block_line - 1) // 2
    if N % 2 == 0:
        even_diag_blocks = (completed_diag_block_line + 1) // 2
        odd_diag_blocks = total_completed_diag_blocks - even_diag_blocks
    else:
        odd_diag_blocks = (completed_diag_block_line + 1) // 2
        even_diag_blocks = total_completed_diag_blocks - odd_diag_blocks

    score += 4 * odd_diag_blocks * lower_left[-1] + 4 * even_diag_blocks * lower_left[-2]

    remaining_diagonal_blocks = completed_diag_block_line + 1
    score += remaining_diagonal_blocks * (
            lower_left[rem_diag_blocks]
            + lower_right[rem_diag_blocks]
            + upper_left[rem_diag_blocks]
            + upper_right[rem_diag_blocks])

    print(score)

    reps = 2
    part_two_grid = np.tile(input_grid == 1, (2*reps+1, 2*reps+1)).astype(int)
    part_two_grid[65 + reps * input_grid.shape[0], 65 + reps * input_grid.shape[1]] = 2

    positions = (part_two_grid == 2)
    wall_grid = (part_two_grid == 1)
    for _ in range(N):
        positions = step(positions, wall_grid)