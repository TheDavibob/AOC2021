# /// script
# dependencies = [
#   "numpy>=2.0.0",
# ]
# ///

import numpy as np

TEST_DATA = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

with open("data/day_05") as f:
    REAL_DATA = f.read()


def parse_input(puzzle_string):
    top, bottom = puzzle_string.split("\n\n")

    starts = []
    ends = []
    targets = []
    for line in top.split("\n"):
        if line == "":
            continue

        s, e = line.split("-")
        starts.append(int(s))
        ends.append(int(e))

    for line in bottom.split("\n"):
        if line == "":
            continue

        targets.append(int(line))

    return starts, ends, targets


def get_membership(starts, ends, targets):
    s_array = np.array(starts)
    e_array = np.array(ends)
    t_array = np.array(targets)
    is_gt = t_array[:, None] >= s_array[None, :]
    is_lt = t_array[:, None] <= e_array[None, :]
    is_in = is_gt & is_lt
    return is_in


def part_one(puzzle_string):
    starts, ends, targets = parse_input(puzzle_string)
    membership = get_membership(starts, ends, targets)

    return np.any(membership, axis=1).sum()


def part_two(puzzle_string):
    starts, ends, _ = parse_input(puzzle_string)

    # Sort by starts
    index = np.argsort(starts)
    starts = np.array(starts)[index]
    ends = np.array(ends)[index]

    next_start = starts[0]
    next_end = ends[0]
    reduced_intervals = []
    total_length = 0
    for s, e in zip(starts[1:], ends[1:]):
        print(s, e, next_start, next_end)
        if s <= next_end:
            next_end = max(e, next_end)
        else:
            reduced_intervals.append((next_start, next_end))
            total_length += (next_end - next_start) + 1
            next_start = s
            next_end = e

    reduced_intervals.append((next_start, next_end))
    total_length += (next_end - next_start) + 1

    return total_length


if __name__ == "__main__":
    assert part_one(TEST_DATA) == 3
    print(f"Part 1: {part_one(REAL_DATA)}")

    assert part_two(TEST_DATA) == 14
    print(f"Part 2: {part_two(REAL_DATA)}")
    # 348820208020405 is too high: had missed an equality