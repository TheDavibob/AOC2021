import numpy as np
import sympy
from tqdm import tqdm

import common


def parse_input(text):
    instructions = []
    for line in text.split("\n"):
        if line == "":
            continue
        name, extra = line.split(": ")
        parts = extra.split(" ")
        if len(parts) == 1:
            instructions.append((name, "=", int(parts[0])))
        elif len(parts) == 3:
            instructions.append((name, parts[1], (parts[0], parts[2])))
        else:
            raise ValueError("Unexpected length")

    return instructions


def iterate(instructions):
    variables = {}
    paused_instructions = []
    root = None
    for instruction in instructions:
        done_instructions = []
        for paused_instruction in paused_instructions:
            if paused_instruction[2][0] not in variables.keys():
                continue
            if paused_instruction[2][1] not in variables.keys():
                continue

            arg0 = variables[paused_instruction[2][0]]
            arg1 = variables[paused_instruction[2][1]]
            variables[paused_instruction[0]] = eval(str(arg0) + paused_instruction[1] + str(arg1))
            if paused_instruction[0] == "root":
                return variables[paused_instruction[0]]
            done_instructions.append(paused_instruction)

        for done in done_instructions:
            paused_instructions.remove(done)

        if instruction[1] == "=":
            variables[instruction[0]] = instruction[2]
        else:
            if instruction[2][0] not in variables.keys():
                paused_instructions.append(instruction)
                continue
            if instruction[2][1] not in variables.keys():
                paused_instructions.append(instruction)
                continue

            arg0 = variables[instruction[2][0]]
            arg1 = variables[instruction[2][1]]
            variables[instruction[0]] = eval(str(arg0) + instruction[1] + str(arg1))
            if instruction[0] == "root":
                return variables[instruction[0]]

    root = variables.get("root", None)
    while root is None:
        done_instructions = []
        for paused_instruction in paused_instructions:
            if paused_instruction[2][0] not in variables.keys():
                continue
            if paused_instruction[2][1] not in variables.keys():
                continue

            arg0 = variables[paused_instruction[2][0]]
            arg1 = variables[paused_instruction[2][1]]
            variables[paused_instruction[0]] = int(eval(str(arg0) + paused_instruction[1] + str(arg1)))
            if paused_instruction[0] == "root":
                return variables[paused_instruction[0]]
            done_instructions.append(paused_instruction)

        for done in done_instructions:
            paused_instructions.remove(done)

    return root


def part_two(instructions):
    # In this, the numbers are represented as rational multiples of the human value
    # plus any known constants
    variables = {}
    paused_instructions = []
    root = None
    for instruction in instructions:
        done_instructions = []
        for paused_instruction in paused_instructions:
            if paused_instruction[2][0] not in variables.keys():
                continue
            if paused_instruction[2][1] not in variables.keys():
                continue

            arg0 = variables[paused_instruction[2][0]]
            arg1 = variables[paused_instruction[2][1]]

            if paused_instruction[0] == "root":
                return arg0, arg1

            variables[paused_instruction[0]] = evaluate_instruction(paused_instruction, arg0, arg1)

            done_instructions.append(paused_instruction)

        for done in done_instructions:
            paused_instructions.remove(done)

        if instruction[1] == "=":
            if instruction[0] == "humn":
                variables["humn"] = ((1, 1), 0)
            else:
                variables[instruction[0]] = ((0, 1), instruction[2])
        else:
            if instruction[2][0] not in variables.keys():
                paused_instructions.append(instruction)
                continue
            if instruction[2][1] not in variables.keys():
                paused_instructions.append(instruction)
                continue

            arg0 = variables[instruction[2][0]]
            arg1 = variables[instruction[2][1]]

            if instruction[0] == "root":
                return arg0, arg1

            variables[instruction[0]] = evaluate_instruction(instruction, arg0, arg1)

    root = variables.get("root", None)
    while root is None:
        done_instructions = []
        for paused_instruction in paused_instructions:
            if paused_instruction[2][0] not in variables.keys():
                continue
            if paused_instruction[2][1] not in variables.keys():
                continue

            arg0 = variables[paused_instruction[2][0]]
            arg1 = variables[paused_instruction[2][1]]

            if paused_instruction[0] == "root":
                return arg0, arg1

            variables[paused_instruction[0]] = evaluate_instruction(paused_instruction, arg0, arg1)

            done_instructions.append(paused_instruction)

        for done in done_instructions:
            paused_instructions.remove(done)

    return root


def evaluate_instruction(instruction, arg0, arg1):
    if arg0[0][0] != 0:
        ...

    if arg1[0][0] != 0:
        ...

    if instruction[1] == "+":
        out = (
            (
                arg0[0][0] * arg1[0][1] + arg1[0][0] * arg0[0][1],
                arg1[0][1] * arg0[0][1]
            ),
            arg0[1] + arg1[1]
        )
    elif instruction[1] == "-":
        out = (
            (
                arg0[0][0] * arg1[0][1] - arg1[0][0] * arg0[0][1],
                arg1[0][1] * arg0[0][1]
            ),
            arg0[1] - arg1[1]
        )
    elif instruction[1] == "*":
        if arg1[0][0] == 0:
            out = (
                (arg0[0][0] * arg1[1], arg0[0][1]),
                arg0[1] * arg1[1]
            )
        elif arg0[0][0] == 0:
            out = (
                (arg1[0][0] * arg0[1], arg1[0][1]),
                arg0[1] * arg1[1]
            )
        else:
            raise ValueError("Strange mulitplicand")
    elif instruction[1] == "/":
        assert arg1[0][0] == 0
        out = (
            (arg0[0][0], arg0[0][1] * arg1[1]),
            arg0[1] // arg1[1]
        )

    if out[0][0] == 0:
        out = ((0, 1), out[1])

    if out[0] != (0, 1):
        print(out)

    return out


example = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""


if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    instructions = parse_input(text)
    root = iterate(instructions)
    common.part(1, root)

    arg0, arg1 = part_two(instructions)
    # This gives a/b * humn + c = d, so solve. We know that arg1[0] = (0, 1)
    common.part(2, (arg1[1] - arg0[1]) * arg0[0][1] // arg0[0][0])
