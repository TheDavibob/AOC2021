import numpy as np
import common


def parse_input(text):
    crates = {n+1: [] for n in range(9)}

    for line in text.split("\n")[:8]:
        for i in range(9):
            if len(line) < 4*i + 1:
                continue
            if (crate := line[4*i+1]) != " ":
                crates[i+1].append(crate)

    for i in range(9):
        crates[i+1] = crates[i+1][::-1]

    instructions = []
    for line in text.split("\n")[10:]:
        if line == "":
            continue

        n, f, t = line.split(" ")[1::2]
        instructions.append((n, f, t))

    return crates, instructions


def step(crates, n_crates, from_stack, to_stack):
    for _ in range(int(n_crates)):
        crates[int(to_stack)].append(crates[int(from_stack)].pop())

    return crates


def step_2(crates, n_crates, from_stack, to_stack):
    moved_crates = []
    for _ in range(int(n_crates)):
        moved_crates.append(crates[int(from_stack)].pop())

    for _ in range(int(n_crates)):
        crates[int(to_stack)].append(moved_crates.pop())

    return crates



if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    crates, instructions = parse_input(text)
    for instruction in instructions:
        step(crates, *instruction)
    out = "".join([crates[i+1][-1] for i in range(9)])

    common.part(1, out)

    crates, instructions = parse_input(text)
    for instruction in instructions:
        step_2(crates, *instruction)
    out = "".join([crates[i+1][-1] for i in range(9)])
    common.part(2, out)
