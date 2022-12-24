import dataclasses
import sys

import numpy as np
import common


def parse_input(text):
    lines = [line for line in text.split("\n") if line != ""]
    height = len(lines) - 2
    width = len(lines[0]) - 2
    arrays = {
        dir: np.zeros((height, width), dtype=int)
        for dir in "><^v"
    }

    entry_exit = []
    for i_line, line in enumerate(lines):
        for i_char, char in enumerate(line):
            if ((i_line == 0) or (i_line == height+1)) and (char == "."):
                entry_exit.append((i_line - 1, i_char - 1))

            if char not in [".", "#"]:
                arrays[char][i_line-1, i_char-1] += 1

    return arrays, entry_exit


def step_arrays(arrays):
    new_arrays = {}
    for direction, array in arrays.items():
        if direction == "^":
            new_array = np.roll(array, -1, axis=0)
        elif direction == "v":
            new_array = np.roll(array, 1, axis=0)
        elif direction == "<":
            new_array = np.roll(array, -1, axis=1)
        elif direction == ">":
            new_array = np.roll(array, 1, axis=1)
        else:
            raise ValueError("Unexpected direction")

        new_arrays[direction] = new_array

    return new_arrays


def step_arrays_2(arrays):
    new_arrays = {}
    for direction, array in arrays.items():
        if direction == "^":
            new_array = np.zeros_like(array)
            new_array[1:-1, 1:-1] = np.roll(array[1:-1, 1:-1], -1, axis=0)
        elif direction == "v":
            new_array = np.zeros_like(array)
            new_array[1:-1, 1:-1] = np.roll(array[1:-1, 1:-1], 1, axis=0)
        elif direction == "<":
            new_array = np.zeros_like(array)
            new_array[1:-1, 1:-1] = np.roll(array[1:-1, 1:-1], -1, axis=1)
        elif direction == ">":
            new_array = np.zeros_like(array)
            new_array[1:-1, 1:-1] = np.roll(array[1:-1, 1:-1], 1, axis=1)
        elif direction == ".":
            new_array = array
        else:
            raise ValueError("Unexpected direction")

        new_arrays[direction] = new_array

    return new_arrays


DIR_NAMES = {
    "D": np.array([1, 0], dtype=int),
    "R": np.array([0, 1], dtype=int),
    "U": np.array([-1, 0], dtype=int),
    "L": np.array([0, -1], dtype=int),
    "W": np.array([0, 0], dtype=int),
}


def all_moves(current_position, next_blizzard, pref_order=None):
    if pref_order is None:
        pref_order = "DRULW"

    options = []

    blizzard_map = np.sum([dir_map for dir_map in next_blizzard.values()], axis=0)
    blizzard_shape = np.array(next_blizzard[">"].shape)

    for option in pref_order:
        displacement = DIR_NAMES[option]
        proposed_position = current_position + displacement

        if any(proposed_position < 0):
            continue

        if any(proposed_position >= blizzard_shape):
            continue

        if blizzard_map[tuple(proposed_position)] == 0:
            options.append(option)

    return options


@dataclasses.dataclass
class Pointer:
    value: float


@dataclasses.dataclass
class Cache:
    lookup: dict


def len_to_exit(current_position, end_position, arrays, current_distance, best_so_far, cache):
    if current_distance >= best_so_far.value:
        return 0

    cache_state = (tuple(current_position), current_distance)
    if (cached := cache.lookup.get(cache_state, None)) is not None:
        return cached

    print(current_distance, current_position, best_so_far.value)

    if np.all(current_position == end_position):
        if current_distance + 1 < best_so_far.value:
            best_so_far.value = current_distance + 1
        return 1  # 1 more step to the exit I go

    next_blizzard = step_arrays(arrays)
    options = all_moves(current_position, next_blizzard)
    if len(options) == 0:
        return 0

    best_distance = 0
    for option in options:
        new_position = current_position + DIR_NAMES[option]
        distance = len_to_exit(new_position, end_position, next_blizzard, current_distance + 1, best_so_far, cache)
        if distance > 0:
            if best_distance == 0:
                best_distance = distance + 1
            if distance + 1 < best_distance:
                best_distance = distance + 1

    cache.lookup[cache_state] = best_distance

    return best_distance


demo_array = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

def from_start(arrays, entry_exit):
    start_postition = np.array(entry_exit[0], dtype=int)
    end_position = np.array(entry_exit[1], dtype=int) - np.array([1, 0], dtype=int)

    best_so_far = Pointer(value=100000)

    return len_to_exit(start_postition, end_position, arrays, 0, best_so_far, Cache(lookup={}))


def len_to_exit_2(current_position, targets, arrays, current_distance, best_so_far, cache, pref_orders):
    manhattan_remaining = np.sum(np.abs(current_position - targets[0]))
    for t0, t1 in zip(targets[:-1], targets[1:]):
        manhattan_remaining += np.sum(np.abs(t0 - t1))

    if (current_distance + manhattan_remaining) >= best_so_far.value:
        return -1

    cache_state = (tuple(current_position), current_distance, len(targets))
    if (cached := cache.lookup.get(cache_state, None)) is not None:
        return cached

    if np.all(current_position == targets[0]):
        print(current_distance, current_position, len(targets), best_so_far.value)
        new_targets = targets[1:]
        pref_orders = pref_orders[1:]
        if not new_targets:
            if current_distance < best_so_far.value:
                best_so_far.value = current_distance
            return 0
    else:
        new_targets = targets

    next_blizzard = step_arrays_2(arrays)
    options = all_moves(current_position, next_blizzard, pref_orders[0])
    if len(options) == 0:
        return -1

    best_distance = -1
    for option in options:
        new_position = current_position + DIR_NAMES[option]
        distance = len_to_exit_2(new_position, new_targets, next_blizzard, current_distance + 1, best_so_far, cache, pref_orders)
        if distance > -1:
            if best_distance == -1:
                best_distance = distance + 1
            if distance + 1 < best_distance:
                best_distance = distance + 1

    cache.lookup[cache_state] = best_distance

    return best_distance


def from_start_to_end_to_start(arrays, entry_exit):
    start_postition = np.array(entry_exit[0], dtype=int) + 1
    end_position = np.array(entry_exit[1], dtype=int) + 1
    for dir, array in arrays.items():
        new_array = np.zeros((array.shape[0]+2, array.shape[1]+2))
        new_array[1:-1, 1:-1] = array
        arrays[dir] = new_array

    wall_array = np.ones(new_array.shape)
    wall_array[1:-1, 1:-1] = 0
    wall_array[tuple(start_postition)] = 0
    wall_array[tuple(end_position)] = 0
    arrays["."] = wall_array

    best_so_far = Pointer(value=1500)

    return len_to_exit_2(
        start_postition,
        [end_position, start_postition, end_position],
        arrays,
        0,
        best_so_far,
        Cache(lookup={}),
        ["DRLWU", "ULRWD", "DRLWU"]
    )


if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    arrays, entry_exit = parse_input(text)

    # distance = from_start(arrays, entry_exit)
    #
    # common.part(1, distance)

    sys.setrecursionlimit(1600)
    distance = from_start_to_end_to_start(arrays, entry_exit)
    common.part(2, distance)
