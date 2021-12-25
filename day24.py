import sympy as sym

import common
import numpy as np


ARGS_MAP = {
    "w": 0,
    "x": 1,
    "y": 2,
    "z": 3
}


class ALP:
    def __init__(self):
        self.state = [0, 0, 0, 0]

    def step(self, instruction, next_input):
        progress = False
        if instruction == "":
            return

        code, *args = instruction.split(' ')

        if len(args) > 1:
            if args[1] in ARGS_MAP.keys():
                value = self.state[ARGS_MAP[args[1]]]
            else:
                value = int(args[1])

        if code == "inp":
            print(self.state)
            if next_input is None:
                print(f"Stopped at {self.state}")
                raise ValueError()
            self.state[ARGS_MAP[args[0]]] = next_input
            progress = True
        elif code == "add":
            self.state[ARGS_MAP[args[0]]] += value
        elif code == "mul":
            self.state[ARGS_MAP[args[0]]] *= value
        elif code == "div":
            self.state[ARGS_MAP[args[0]]] //= value
        elif code == "mod":
            self.state[ARGS_MAP[args[0]]] %= value
        elif code == "eql":
            self.state[ARGS_MAP[args[0]]] = int(self.state[ARGS_MAP[args[0]]] == value)
        else:
            raise ValueError("Code not understood")

        return progress

    def step_all(self, instructions, input_string, initial_state=None):
        if initial_state is None:
            self.state = [0, 0, 0, 0]
        else:
            self.state = initial_state
        position = 0
        for instruction in instructions.split('\n'):
            if position == len(input_string):
                new_input = None
            else:
                new_input = input_string[position]
            progress = self.step(instruction, new_input)
            if progress:
                position += 1


def chunk_input(text):
    quotients = []
    x_adds = []
    y_adds = []
    for val in range(14):
        q, x, y = parse_block(text.split('\n')[18*val:18*(val+1)])
        quotients.append(q)
        x_adds.append(x)
        y_adds.append(y)

    return quotients, x_adds, y_adds


def parse_block(block):
    target = """inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 5
mul y x
add z y"""
    for line_block, line_target in zip(block, target.split('\n')):
        if line_target == 'div z 1':
            quotient = int(line_block.split(' ')[-1])
        elif line_target == "add x 10":
            x_add = int(line_block.split(' ')[-1])
        elif line_target == "add y 5":
            y_add = int(line_block.split(' ')[-1])
        else:
            assert line_block == line_target

    return quotient, x_add, y_add


def simple_calc(z, I, q, x, y):
    if z % 26 + x == I:
        return z // q
    else:
        return 26*(z // q) + (I + y)


def back_propogate(prior_z, q, x, y):
    valids = []
    for posterior_z in range(q*(prior_z+1)):
        for I in range(1, 10):
            if simple_calc(posterior_z, I, q, x, y) == prior_z:
                valids.append((I, posterior_z))

    return valids


def all_back_propogate(quotient, x_add, y_add, n_blocks=14):
    final_state = [[(0, 0)]]
    state = final_state
    for i in range(n_blocks):
        print(i)
        q = quotient[-(i+1)]
        x = x_add[-(i+1)]
        y = y_add[-(i+1)]
        new_state = []
        for s in state:
            previous_state = s[-1][-1]
            valid_new_states = back_propogate(previous_state, q, x, y)
            for v in valid_new_states:
                new_state.append(s + [v])
        state = new_state

    return state


def forward_propogate(quotient, x_add, y_add, n_blocks=14):
    initial_state = [[(0, 0)]]
    state = initial_state
    for i in range(n_blocks):
        print(i)
        q = quotient[i]
        x = x_add[i]
        y = y_add[i]
        new_state = []
        for s in state:
            previous_state = s[-1][-1]
            for I in range(1, 10):
                fp = simple_calc(previous_state, I, q, x, y)
                new_state.append(s + [(I, fp)])

        state = new_state

    return state


def combine_propogations(q, x, y):
    bp_states = all_back_propogate(q, x, y, n_blocks=8)
    fp_states = forward_propogate(q, x, y, n_blocks=6)
    bp_final_states = [b[-1][-1] for b in bp_states]
    fp_final_states = [b[-1][-1] for b in fp_states]
    valid_intermediate_states = []
    for i in range(max(bp_final_states)):
        if (i in bp_final_states) and (i in fp_final_states):
            valid_intermediate_states.append(i)

    valid_instructions = []
    for s in valid_intermediate_states:
        full_forward = [f for f in fp_states if f[-1][-1] == s]
        forward_instructions = []
        for f in full_forward:
            instructions = [g[0] for g in f[1:]]
            forward_instructions.append(instructions)

        full_backward = [f for f in bp_states if f[-1][-1] == s]
        backward_instructions = []
        for f in full_backward:
            instructions = [g[0] for g in reversed(f[1:])]
            backward_instructions.append(instructions)

        for f in forward_instructions:
            for b in backward_instructions:
                valid_instructions.append(f + b)

    return valid_instructions


def get_best_instructions(valid_instructions):
    intstruction = [int("".join(str(j) for j in i)) for i in valid_instructions]
    return max(intstruction), min(intstruction)


if __name__ == "__main__":
    text = common.import_file('input/day24_input')
    q, x, y = chunk_input(text)
    valid_instructions = combine_propogations(q, x, y)
    maximum, minimum = get_best_instructions(valid_instructions)
    print(f"Part 1: {maximum}")
    print(f"Part 2: {minimum}")
