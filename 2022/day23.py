import numpy as np
from tqdm import tqdm

import common


def parse_input(text):
    lines = [l for l in text.split("\n") if l != ""]

    elves = []
    for i_row, line in enumerate(lines):
        for i_col, char in enumerate(line):
            if char == "#":
                elves.append((i_row, i_col))

    return elves


DIRECTIONS = np.array((
    (-1, -1),  # NW
    (-1, 0),  # N
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1)
), dtype=int)


SINGLE_DIR = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1)
}


FREE_LOOK = {
    "N": slice(0, 3),
    "E": slice(2, 5),
    "S": slice(4, 7),
    "W": slice(6, 9)
}


ORDER = {
    "N": "NSWE",
    "S": "SWEN",
    "W": "WENS",
    "E": "ENSW"
}


def step(elves, start_dir):
    proposed_moves = {}
    for elf in elves:
        adj = []
        for direction in DIRECTIONS:
            shifted = np.array(elf) + direction
            adj.append(tuple(shifted) in elves)

        if not any(adj):
            proposed_moves[elf] = elf
        else:
            proposed_moves[elf] = elf
            for dir in ORDER[start_dir]:
                indices = FREE_LOOK[dir]
                adj_dir = adj[indices]
                if dir == "W":
                    adj_dir.append(adj[0])
                if not any(adj_dir):
                    shifted = np.array(elf) + np.array(SINGLE_DIR[dir])
                    proposed_moves[elf] = tuple(shifted)
                    break

    # Part 2: actually do the moves
    all_proposed_moves = list(proposed_moves.values())
    moves_to_decline = []
    for move in all_proposed_moves:
        if all_proposed_moves.count(move) > 1:
            if move not in moves_to_decline:
                moves_to_decline.append(move)

    for elf, move in proposed_moves.items():
        if move in moves_to_decline:
            proposed_moves[elf] = elf

    return list(proposed_moves.values())


">3184, < 5xxx"


def step_n(elves, n):
    sequence = "NSWE"
    print_elves(elves)
    for i in tqdm(range(n)):
        red_i = i % len(sequence)
        direction = sequence[red_i]

        elves = step(elves, direction)
        print_elves(elves)

    return elves


def part_two(elves):
    changed = True
    counter = 0
    sequence = "NSWE"
    while changed:
        red_i = counter % len(sequence)
        direction = sequence[red_i]

        new_elves = step(elves, direction)
        if new_elves == elves:
            changed = False

        elves = new_elves
        counter += 1

        if counter % 10 == 0:
            print(counter)

    return counter


def count_elves(elves):
    max_height = max(elf[0] for elf in elves)
    min_height = min(elf[0] for elf in elves)
    max_width = max(elf[1] for elf in elves)
    min_width = min(elf[1] for elf in elves)

    width = max_width - min_width + 1
    height = max_height - min_height + 1

    area = width * height

    free_area = area - len(elves)

    return free_area


def print_elves(elves):
    max_height = max(elf[0] for elf in elves)
    min_height = min(elf[0] for elf in elves)
    max_width = max(elf[1] for elf in elves)
    min_width = min(elf[1] for elf in elves)

    for i in range(min_height, max_height + 1):
        line = ""
        for j in range(min_width, max_width + 1):
            if (i, j) in elves:
                line += "#"
            else:
                line += "."
        print(line)


small_sample = """.....
..##.
..#..
.....
..##.
....."""

larger_sample = """..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
.............."""


if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    elves = parse_input(text)

    # elves = step_n(elves, 10)

    # common.part(1, count_elves(elves))

    elves = parse_input(text)
    common.part(2, part_two(elves))
