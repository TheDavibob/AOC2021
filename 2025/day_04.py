# /// script
# dependencies = [
#   "numpy>=2.0.0",
#   "scipy",
# ]
# ///

import numpy as np
from scipy.signal import convolve2d


TEST_DATA = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

with open("data/day_04") as f:
    REAL_DATA = f.read()


def puzzle_input_to_array(puzzle_input):
    lines = [line for line in puzzle_input.split("\n") if line != ""]
    height = len(lines)
    width = len(lines[0])

    char_map = {".": 0, "@": 1}

    array = np.zeros((height, width), dtype=int)

    for i_line, line in enumerate(lines):
        for i_col, char in enumerate(line):
            array[i_line, i_col] = char_map[char]

    return array


def count_neighbours(array):
    kernel = np.ones((3, 3), dtype=int)
    kernel[1, 1] = 0

    neighbour_count = convolve2d(array, kernel, mode="same")

    return np.sum((neighbour_count < 4) & array)


def part_one(puzzle_input):
    array = puzzle_input_to_array(puzzle_input)
    accessible = count_neighbours(array)
    return accessible


def iterate(array):
    kernel = np.ones((3, 3), dtype=int)
    kernel[1, 1] = 0

    neighbour_count = convolve2d(array, kernel, mode="same")

    to_remove = (neighbour_count < 4) & array

    if not np.any(to_remove):
        raise StopIteration

    count = np.sum(to_remove.astype(int))

    new_array = array * (1-to_remove)
    return new_array, count


def part_two(puzzle_input):
    array = puzzle_input_to_array(puzzle_input)
    removed_els = 0

    while True:
        try:
            array, count = iterate(array)
        except StopIteration:
            break

        removed_els += count

    return removed_els

if __name__ == "__main__":
    assert part_one(TEST_DATA) == 13
    print(f"Part 1: {part_one(REAL_DATA)}")

    assert part_two(TEST_DATA) == 43
    print(f"Part 2: {part_two(REAL_DATA)}")