import math
from copy import copy

import numpy as np

import common

def parse_input(text):
    top, bottom = text.split("\n\n")
    instructions = top

    mapping = {}
    for line in bottom.split("\n"):
        if line == "":
            continue
        f, t = line.split(" = ")
        t1, t2 = t[1:-1].split(", ")
        mapping[f] = (t1, t2)

    return instructions, mapping


def part_one(instructions, mapping):
    position = "AAA"
    n_steps = 0

    while position != "ZZZ":
        next_instruction = ["L", "R"].index(instructions[n_steps % len(instructions)])
        position = mapping[position][next_instruction]
        n_steps += 1

    common.part(1, n_steps)


def part_two(instructions, mapping):
    starts = [x for x in mapping.keys() if x[-1] == "A"]
    ends = [x for x in mapping.keys() if x[-1] == "Z"]

    all_path_lengths = []
    for s in starts:
        all_path_lengths.append(path_length(s, ends, instructions))
        # print(s, all_path_lengths[-1])

    # I'm not sure *why* these are periodic, but once you've established it for
    # the first case it's obviously true
    period = [x[0] for x in all_path_lengths]
    lcm = 1
    for p in period:
        lcm = math.lcm(lcm, p)

    common.part(2, lcm)

    return all_path_lengths


def path_length(start, finishes, instructions, offset=0, n_reps=10):
    position = start
    n_steps = 0
    path_lengths = []

    while True:
        next_instruction = ["L", "R"].index(instructions[(n_steps+offset) % len(
            instructions)])
        position = mapping[position][next_instruction]
        n_steps += 1

        if position in finishes:
            path_lengths.append(copy(n_steps))

        if len(path_lengths) == n_reps:
            return path_lengths


if __name__ == "__main__":
    text = common.import_file("input/day8")
    instructions, mapping = parse_input(text)
    part_one(instructions, mapping)
    out = part_two(instructions, mapping)