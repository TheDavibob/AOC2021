# /// script
# dependencies = [
#   "numpy>=2.0.0",
# ]
# ///

import numpy as np

TEST_INPUT = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

with open("data/day_07") as f:
    REAL_INPUT = f.read()


def step(current_locs: set[int], split_locs: list[int]):
    to_remove = set()
    to_add = set()
    for split_loc in split_locs:
        if split_loc in current_locs:
            to_remove.add(split_loc)
            to_add.add(split_loc-1)
            to_add.add(split_loc+1)

    count = len(to_remove)  # maybe

    return (current_locs - to_remove).union(to_add), count


def part_one(puzzle_input):
    lines = puzzle_input.split("\n")
    start_loc = set(i for i, l in enumerate(lines[0]) if l == "S")

    current_locs = start_loc
    total_count = 0
    for line in lines[1:]:
        split_loc = [i for i, l in enumerate(line) if l == "^"]
        if split_loc:
            current_locs, count = step(current_locs, split_loc)
            total_count += count
        print(current_locs, total_count)

    return total_count


def part_two(puzzle_input):
    lines = puzzle_input.split("\n")
    possible_locs = [i for i, l in enumerate(lines[0]) if l == "S"]
    count = np.zeros(len(lines[0]), dtype=int)
    count[possible_locs[0]] = 1

    for line in lines[1:]:
        split_loc = [i for i, l in enumerate(line) if l == "^"]
        if split_loc:
            new_count = count.copy()
            for loc in split_loc:
                c = count[loc]
                new_count[loc-1] += c
                new_count[loc+1] += c
                new_count[loc] -= c
            count = new_count

    return count.sum()

if __name__ == "__main__":
    assert part_one(TEST_INPUT) == 21
    print(f"Part 1: {part_one(REAL_INPUT)}")

    assert part_two(TEST_INPUT) == 40
    print(f"Part 2: {part_two(REAL_INPUT)}")