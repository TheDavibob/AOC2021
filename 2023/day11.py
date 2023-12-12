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

import common
import numpy as np


def parse_input(text):
    return common.convert_string_to_np_array(text, {".": 0, "#": 1}).astype(int)


def expand(array):
    expand_row = []
    expand_col = []
    for i_row in range(array.shape[0]):
        if not np.any(array[i_row]):
            expand_row.append(i_row)

    for i_col in range(array.shape[1]):
        if not np.any(array[:, i_col]):
            expand_col.append(i_col)

    n_row_exp = 0
    n_col_exp = 0
    for i_row in expand_row:
        array = np.insert(array, i_row + n_row_exp, np.zeros(array.shape[1]), axis=0)
        n_row_exp += 1

    for i_col in expand_col:
        array = np.insert(array, i_col + n_col_exp, np.zeros(array.shape[0]), axis=1)
        n_col_exp += 1

    return array


def get_expansion_rows_only(array):
    expand_row = []
    expand_col = []
    for i_row in range(array.shape[0]):
        if not np.any(array[i_row]):
            expand_row.append(i_row)

    for i_col in range(array.shape[1]):
        if not np.any(array[:, i_col]):
            expand_col.append(i_col)

    return expand_row, expand_col


def part_one(grid):
    grid = expand(grid)

    total_length = 0
    all_points = np.argwhere(grid)
    for point_0 in all_points:
        for point_1 in all_points:
            total_length += np.sum(np.abs(point_0 - point_1))

    common.part(1, total_length // 2)


def part_two(grid, n_expansion=1000000):
    expansion_rows, expansion_cols = get_expansion_rows_only(grid)
    all_points = np.argwhere(grid)

    total_length = 0
    for point_0 in all_points:
        for point_1 in all_points:
            flat_length = np.sum(np.abs(point_0 - point_1))

            n_rows_between = np.sum(
                (min(point_0[0], point_1[0]) < expansion_rows)
                & (max(point_0[0], point_1[0]) > expansion_rows)
            )
            n_cols_between = np.sum(
                (min(point_0[1], point_1[1]) < expansion_cols)
                & (max(point_0[1], point_1[1]) > expansion_cols)
            )

            total_length += flat_length + (n_expansion-1)*(n_rows_between +
                                                          n_cols_between)

    common.part(2, total_length // 2)


if __name__ == "__main__":
    text = common.import_file("input/day11")

    text_0 = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

    grid = parse_input(text)
    part_one(grid)
    part_two(grid, 1000000)