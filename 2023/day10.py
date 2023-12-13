import math

import numpy as np
from matplotlib import pyplot as plt

import common


INT = {
    ".": 0,
    "S": 255,
    "|": 1,
    "-": 2,
    "L": 3,
    "J": 4,
    "7": 5,
    "F": 6,
}


def parse_input(text):
    return common.convert_string_to_np_array(
        text,
        INT
    ).astype(int)


def get_one_cell_validity(map):
    is_valid = np.ones(map.shape, dtype=bool)
    is_valid[map == INT["."]] = 0
    total_valid = np.sum(is_valid)

    connected_above = (map == INT["L"]) | (map == INT["J"]) | (map == INT["|"]) | (map == INT["S"])
    connected_below = (map == INT["7"]) | (map == INT["F"]) | (map == INT["|"]) | (map == INT["S"])
    connected_right = (map == INT["L"]) | (map == INT["F"]) | (map == INT["-"]) | (map == INT["S"])
    connected_left = (map == INT["7"]) | (map == INT["J"]) | (map == INT["-"]) | (map == INT["S"])

    while True:
        connected_above &= is_valid
        connected_below &= is_valid
        connected_right &= is_valid
        connected_left &= is_valid

        is_valid[:, 1:] &= ~connected_left[:, 1:] | (connected_left[:, 1:] & connected_right[:, :-1])
        is_valid[:, :-1] &= ~connected_right[:, :-1] | (connected_left[:, 1:] & connected_right[:, :-1])
        is_valid[1:] &= ~connected_above[1:] | (connected_above[1:] & connected_below[:-1])
        is_valid[:-1] &= ~connected_below[:-1] | (connected_above[1:] & connected_below[:-1])

        is_valid[0] &= ~connected_above[0]
        is_valid[-1] &= ~connected_below[-1]

        is_valid[:, 0] &= ~connected_left[:, 0]
        is_valid[:, -1] &= ~connected_right[:, -1]

        is_valid[map == INT["S"]] = 1

        if np.sum(is_valid) == total_valid:
            break
        else:
            total_valid = np.sum(is_valid)

    return is_valid


def find_loop(map, starting_point):

    chain = []
    is_complete = False
    chain.append(starting_point)
    while True:
        map_coord = chain[-1]
        map_val = map[map_coord]

        valid_targets = []

        if map_val == INT["S"]:
            chain = chain[::-1]
            continue

        if map_val in [INT["L"], INT["J"], INT["|"]]:
            if map_coord[0] == 0:
                continue

            valid_targets.append((map_coord[0]-1, map_coord[1]))

        if map_val in [INT["F"], INT["7"], INT["|"]]:
            if map_coord[0] == map.shape[0]-1:
                continue

            valid_targets.append((map_coord[0] + 1, map_coord[1]))

        if map_val in [INT["L"], INT["F"], INT["-"]]:
            if map_coord[1] == map.shape[1]-1:
                continue

            valid_targets.append((map_coord[0], map_coord[1]+1))

        if map_val in [INT["7"], INT["J"], INT["-"]]:
            if map_coord[1] == 0:
                continue

            valid_targets.append((map_coord[0], map_coord[1]-1))

        if len(valid_targets) != 2:
            break

        new_target = False
        for v in valid_targets:
            if v not in chain:
                new_target = True
                chain.append(v)
                break

        if not new_target:
            is_complete = True
            break

    return chain, is_complete


def remove_all_incomplete_chains(map, is_valid):
    total_valid = np.sum(is_valid)
    valid_chains = []

    while True:
        starting_points = np.where(is_valid)
        start_point = starting_points[0][0], starting_points[1][0]
        if map[start_point] == INT["S"]:
            start_point = starting_points[0][1], starting_points[1][1]

        chain, is_complete = find_loop(map, start_point)

        if is_complete:
            valid_chains.append(chain)

        for c in chain:
            is_valid[c] = 0

        if np.sum(is_valid) == total_valid:
            break
        else:
            total_valid = np.sum(is_valid)

        if total_valid <= 1:
            break

    return valid_chains


def get_best_chain(map, chains):
    S_loc = (np.where(map == INT["S"])[0][0], np.where(map == INT["S"])[1][0])
    target_chain = None
    for chain in chains:
        if S_loc in chain:
            target_chain = chain
            break
    return target_chain

def part_one(map):
    is_valid = get_one_cell_validity(map)
    chains = remove_all_incomplete_chains(map, is_valid)

    target_chain = get_best_chain(map, chains)

    common.part(1, len(target_chain) // 2)


def mark_immediate_outside(map, chain):
    # This puts the outside on the left side of the chain as we go along
    inside_outside_map = np.zeros_like(map)
    for c in chain:
        inside_outside_map[c] = 255

    for prev, current in zip(chain[1:], chain[:-1]):
        outside_targets = []
        inside_targets = []
        if prev[0] == current[0] + 1:
            # outside is "left"
            outside_targets.append((current[0], current[1]-1))
            outside_targets.append((prev[0], prev[1]-1))

            inside_targets.append((current[0], current[1]+1))
            inside_targets.append((prev[0], prev[1]+1))
        elif prev[0] == current[0] - 1:
            # outside is "right"
            outside_targets.append((current[0], current[1]+1))
            inside_targets.append((current[0], current[1]-1))

            outside_targets.append((prev[0], prev[1]+1))
            inside_targets.append((prev[0], prev[1]-1))
        elif prev[1] == current[1] + 1:
            # outside is "below"
            outside_targets.append((current[0]+1, current[1]))
            inside_targets.append((current[0]-1, current[1]))
            outside_targets.append((prev[0]+1, prev[1]))
            inside_targets.append((prev[0]-1, prev[1]))
        elif prev[1] == current[1] - 1:
            # outside is "above"
            outside_targets.append((current[0]-1, current[1]))
            inside_targets.append((current[0]+1, current[1]))
            outside_targets.append((prev[0]-1, prev[1]))
            inside_targets.append((prev[0]+1, prev[1]))

        for outside_target in outside_targets:
            if outside_target[0] < 0 or outside_target[0] >= map.shape[0]:
                outside_targets.remove(outside_target)
            elif outside_target[1] < 0 or outside_target[1] >= map.shape[1]:
                outside_targets.remove(outside_target)

        for inside_target in inside_targets:
            if inside_target[0] < 0 or inside_target[0] >= map.shape[0]:
                inside_targets.remove(inside_target)
            elif inside_target[1] < 0 or inside_target[1] >= map.shape[1]:
                inside_targets.remove(inside_target)

        for inside_target in inside_targets:
            if inside_target not in chain:
                inside_outside_map[inside_target] = -1

        for outside_target in outside_targets:
            if outside_target not in chain:
                inside_outside_map[outside_target] = 1

    return inside_outside_map


def part_two(map):
    is_valid = get_one_cell_validity(map)
    chains = remove_all_incomplete_chains(map, is_valid)

    target_chain = get_best_chain(map, chains)

    io_map = mark_immediate_outside(map, target_chain)
    io_map = flood_fill(io_map)

    inside_id = -io_map[0, 0]

    common.part(2, np.sum(io_map == inside_id))
    return io_map, target_chain


def flood_fill(io_map):
    n_empty = np.sum(io_map == 0)
    while n_empty > 0:
        for i_row in range(io_map.shape[0]):
            for i_col in range(io_map.shape[1]):
                if io_map[i_row, i_col] != 0:
                    continue

                if i_row > 0 and io_map[i_row-1, i_col] in [-1, 1]:
                    io_map[i_row, i_col] = io_map[i_row-1, i_col]
                elif i_row <= io_map.shape[0]-2 and io_map[i_row+1, i_col] in [-1, 1]:
                    io_map[i_row, i_col] = io_map[i_row+1, i_col]
                elif i_col > 0 and io_map[i_row, i_col-1] in [-1, 1]:
                    io_map[i_row, i_col] = io_map[i_row, i_col-1]
                elif i_col <= io_map.shape[1]-2 and io_map[i_row, i_col+1] in [-1, 1]:
                    io_map[i_row, i_col] = io_map[i_row, i_col+1]

        if np.sum(io_map == 0) == n_empty:
            break
        else:
            n_empty = np.sum(io_map == 0)

    return io_map


if __name__ == "__main__":
    text = common.import_file("input/day10")
    text_0 = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""
    text_1 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""
    text_2 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""
    text_3 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

    map = parse_input(text)

    # part_one(map)
    io_map, chain = part_two(map)