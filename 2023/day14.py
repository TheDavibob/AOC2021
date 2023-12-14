# Copyright (C) Cambridge Consultants Ltd 2023
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import itertools
from functools import cache

import common
import numpy as np
from tqdm import tqdm


def parse_input(text):
    return common.convert_string_to_np_array(
        text,
        {"#": 1, ".": 0, "O": 2}
    )


def tilt_up(grid):
    for i_row in range(grid.shape[0]):
        for i_col in range(grid.shape[1]):
            if grid[i_row, i_col] == 2:
                if grid[i_row-1, i_col] >= 1:
                    continue

                moved = False
                for shift_up in range(1, i_row+1):
                    if grid[i_row-shift_up, i_col] >= 1:
                        grid[i_row, i_col] = 0
                        grid[i_row-shift_up+1, i_col] = 2
                        moved = True
                        break

                if not moved:
                    grid[i_row, i_col] = 0
                    grid[0, i_col] = 2

    return grid


def tilt_down(grid):
    new_grid = grid[::-1]
    tilt_up(new_grid)
    grid[:] = new_grid[::-1]


def tilt_left(grid):
    new_grid = grid.T[:, ::-1]
    tilt_up(new_grid)
    grid[:, :] = new_grid.T[::-1]


def tilt_right(grid):
    new_grid = grid.T[::-1]
    tilt_up(new_grid)
    grid[:] = new_grid.T[:, ::-1]


def part_one(grid):
    tilt_up(grid)

    common.part(1, value(grid))


def value(grid):
    in_row = np.sum(grid==2, axis=1)
    row_value = np.arange(1, grid.shape[0]+1)[::-1]
    return np.dot(in_row, row_value)


def cycle(grid):
    tilt_up(grid)
    tilt_left(grid)
    tilt_down(grid)
    tilt_right(grid)
    return grid


def part_two(grid):

    historic_grids = []

    for n in range(1000000000):
        historic_grids.append(grid.tolist())

        grid = cycle(grid)

        if grid.tolist() in historic_grids:
            break

    cycle_length = n - historic_grids.index(grid.tolist()) + 1

    repeating_pattern = historic_grids[-cycle_length:]
    pattern_start = n-cycle_length

    # Plus 1 as didn't include current grid
    sample_idx = ((1000000000 - pattern_start) % cycle_length)

    new_value = value(np.array(repeating_pattern[sample_idx-1]))

    common.part(2, new_value)


if __name__ == "__main__":
    text = common.import_file("input/day14")

    demo_text = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

    grid = parse_input(text)
    part_one(grid)

    grid = parse_input(text)
    part_two(grid)
