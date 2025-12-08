# /// script
# dependencies = [
#   "numpy>=2.0.0",
# ]
# ///
from math import prod

import numpy as np


TEST_INPUT = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""


with open("data/day_08") as f:
    REAL_DATA = f.read()


def parse_puzzle_input(puzzle_input):
    all_pos = []
    for line in puzzle_input.split("\n"):
        pos = np.array([int(x) for x in line.split(",")])
        all_pos.append(pos)

    return np.array(all_pos)


def get_pairwise_distances(xyz_array):
    pairwise_delta = xyz_array[:, None, :] - xyz_array[None, :, :]

    distances = np.linalg.norm(pairwise_delta, axis=-1)
    distances = np.triu(distances, k=1)
    distances[distances == 0] = np.inf

    return distances


def part_one(puzzle_input, k):
    as_array = parse_puzzle_input(puzzle_input)
    pairwise_distances = get_pairwise_distances(as_array)

    current_sets = []
    for _ in range(k):
        min_index = np.argmin(pairwise_distances)
        to_element, from_element = np.unravel_index(min_index, pairwise_distances.shape)
        pairwise_distances[to_element, from_element] = np.inf
        to_element = tuple(as_array[to_element])
        from_element = tuple(as_array[from_element])

        to_set = None
        from_set = None
        do_anything = True

        for this_set in current_sets:
            if to_element in this_set and from_element in this_set:
                do_anything = False
                break
            if to_element in this_set:
                to_set = this_set
            if from_element in this_set:
                from_set = this_set

        if not do_anything:
            continue

        if to_set is None and from_set is None:
            current_sets.append({to_element, from_element})
        elif to_set is None:
            from_set.add(to_element)
        elif from_set is None:
            to_set.add(from_element)
        else:
            current_sets.remove(to_set)
            current_sets.remove(from_set)
            new_set = to_set.union(from_set)
            current_sets.append(new_set)

        # print([len(s) for s in current_sets])

    return prod(sorted([len(s) for s in current_sets], reverse=True)[:3])


def part_two(puzzle_input):
    as_array = parse_puzzle_input(puzzle_input)
    pairwise_distances = get_pairwise_distances(as_array)

    current_sets = []
    while True:
        min_index = np.argmin(pairwise_distances)
        to_idx, from_idx = np.unravel_index(min_index, pairwise_distances.shape)
        pairwise_distances[to_idx, from_idx] = np.inf
        to_element = tuple(as_array[to_idx])
        from_element = tuple(as_array[from_idx])

        to_set = None
        from_set = None
        do_anything = True

        for this_set in current_sets:
            if to_element in this_set and from_element in this_set:
                do_anything = False
                break
            if to_element in this_set:
                to_set = this_set
            if from_element in this_set:
                from_set = this_set

        if not do_anything:
            continue

        if to_set is None and from_set is None:
            current_sets.append({to_element, from_element})
        elif to_set is None:
            from_set.add(to_element)
        elif from_set is None:
            to_set.add(from_element)
        else:
            current_sets.remove(to_set)
            current_sets.remove(from_set)
            new_set = to_set.union(from_set)
            current_sets.append(new_set)

        if sum(len(s) for s in current_sets) == len(as_array) and len(current_sets) == 1:
            return to_element[0] * from_element[0]



if __name__ == "__main__":
    assert part_one(TEST_INPUT, 10) == 40
    print("Part 1:", part_one(REAL_DATA, 1000))

    assert part_two(TEST_INPUT) == 25272
    # 3052064886 is too low - needed to make sure only had one group oops
    print("Part 2:", part_two(REAL_DATA))