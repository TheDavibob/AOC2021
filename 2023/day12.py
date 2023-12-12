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
    combined = []
    for line in text.split("\n"):
        code, contents = line.split(" ")
        lengths = tuple(int(c) for c in contents.split(","))

        code = common.convert_string_to_np_array(
            code,
            {"?": 2, "#": 1, ".": 0}
        )[0].astype(int)
        combined.append((code, lengths))

    return combined


def part_one(inputs):
    n_combos = 0
    for code, contents in tqdm(inputs):
        # new_count = find_combos(code, contents)
        new_count = count_all_options(code, contents)
        # print(code, contents, new_count)
        n_combos += new_count

    common.part(1, n_combos)


def part_two(inputs):
    n_combos = 0
    for code, contents in tqdm(inputs):
        new_count = count_all_options(np.hstack(5*(code, 2))[:-1], 5*contents)
        # print(code, contents, new_count)
        n_combos += new_count

    common.part(2, n_combos)


def find_combos(code, contents):
    # WORKS BUT IS SLOW
    question_mask = (code == 2)

    n_unfixed = np.sum(question_mask)

    count = 0
    for fix in itertools.product(*([0, 1] for _ in range(n_unfixed))):
        updated_code = code.copy()
        updated_code[question_mask] = fix

        if np.sum(updated_code) != np.sum(contents):
            continue

        blocks = count_blocks(updated_code)

        if blocks == contents:
            count += 1

    return count


def count_blocks(array):
    change = np.diff(np.hstack((0, array, 0)))
    block_length = 0
    block_lengths = []
    for c in change:
        if c == 1:
            block_length = 1
        elif c == 0:
            block_length += 1
        else:
            block_lengths.append(block_length)
            block_length = 0

    return tuple(block_lengths)


@cache
def find_all_locs(array, required_length, min_start_idx):
    # Find all locations where a block of length n can fit within such an
    # array
    locs = []

    array_arr = np.array(array)
    for i in range(min_start_idx, len(array)-required_length+1):
        if np.all(array_arr[i:i+required_length] >= 1):
            locs.append(i)

    return locs


@cache
def count_options(code, lengths, earliest_point) -> int:
    code_arr = np.array(code)
    if len(lengths) == 0:
        if np.any(code_arr[earliest_point:] == 1):
            return 0
        else:
            # print("added")
            return 1

    count = 0
    locs = find_all_locs(code, lengths[0], earliest_point)
    for loc in locs:
        # print(lengths[0], loc)
        if np.any(code_arr[np.maximum(earliest_point, 0):loc] == 1):
            break

        try:
            if code_arr[loc+lengths[0]] == 1:
                continue
        except IndexError:
            pass

        count += count_options(code, lengths[1:], loc+lengths[0]+1)

    return count


def count_all_options(code, contents):
    return count_options(tuple(code), contents, 0)


if __name__ == "__main__":
    text = common.import_file("input/day12")
#     text = """???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1"""
#     text = """????.?#????#?? 2,1,1,3"""
#     text = """#?????.?#???.#.???# 1,2,4,1,1,1"""

    inputs = parse_input(text)
    #
    # for i in inputs[:10]:
    #     print(count_all_options(*i))
    part_one(inputs)
    part_two(inputs)

    # failing_codes = []
    # for input in inputs:
    #     a = count_all_options(*input)
    #     b = find_combos(*input)
    #     if a != b:
    #         failing_codes.append(input)
    #         print(input)

