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
    arrays = []

    for block in text.split("\n\n"):
        if block == "":
            continue

        arrays.append(common.convert_string_to_np_array(
            block,
            {"#": 1, ".": 0}
        ))

    return arrays


def find_reflection(array, skip_val = None):
    for i_col in range(1, array.shape[1]):
        left = array[:, :i_col]
        right = array[:, i_col:]
        left = left[:, ::-1]

        left = left[:, :right.shape[1]]
        right = right[:, :left.shape[1]]

        if np.all(left == right):
            if i_col != skip_val:
                return i_col

    for i_row in range(1, array.shape[0]):
        above = array[:i_row]
        below = array[i_row:]
        above = above[::-1]

        above = above[:below.shape[0]]
        below = below[:above.shape[0]]

        if np.all(above == below):
            if 100*i_row != skip_val:
                return 100*i_row


def find_smudge(array):
    old_reflection_line = find_reflection(array)
    for i_row in range(array.shape[0]):
        for i_col in range(array.shape[1]):
            new_array = array.copy()
            new_array[i_row, i_col] = 1-new_array[i_row, i_col]
            added_weight = find_reflection(new_array, skip_val=old_reflection_line)

            if added_weight is not None:
                return added_weight


def part_one(arrays):
    total = 0
    for array in arrays:
        total += find_reflection(array)

    common.part(1, total)


def part_two(arrays):
    total = 0
    for array in tqdm(arrays):
        total += find_smudge(array)

    common.part(2, total)


if __name__ == "__main__":
    text = common.import_file("input/day13")

    demo_text = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

    arrays = parse_input(text)
    part_one(arrays)
    part_two(arrays)
