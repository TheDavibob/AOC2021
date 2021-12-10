import numpy as np
import common


POINTS_MAP = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}


CLOSE_MAP = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}


COST_MAP = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}


def reduce_line(line):
    for i in range(len(line) - 1):
        if (line[i] in CLOSE_MAP.keys()):
            if CLOSE_MAP[line[i]] == line[i+1]:
                line = line[:i] + line[i+2:]
                break

    return line


def find_corrupt(line):
    len_line = len(line)
    while True:
        old_len = len_line
        line = reduce_line(line)
        len_line = len(line)
        if old_len == len_line:
            break

    for c in line:
        if c in POINTS_MAP.keys():
            return POINTS_MAP[c], line

    return 0, line


def complete_line(line):
    x, reduced_line = find_corrupt(line)
    if x:
        return 0

    return_string = ''
    for c in reduced_line[::-1]:
        return_string += CLOSE_MAP[c]

    score = 0
    for c in return_string:
        score *= 5
        score += COST_MAP[c]

    return score


if __name__ == "__main__":
    text = common.import_file('input/day10_input')

    total = 0
    for line in text.split("\n"):
        total += find_corrupt(line)[0]
    print(f"Part 1: {total}")

    scores = []
    for line in text.split('\n'):
        score = complete_line(line)
        if score:
            scores.append(score)

    print(f"Part 2: {int(np.median(scores))}")