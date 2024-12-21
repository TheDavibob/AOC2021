import functools

adjacency_map = {
    "^": ["A", "v"],
    "A": ["^", ">"],
    "<": ["v"],
    "v": ["<", "^", ">"],
    ">": ["A", "v"],
}

position_map_0 = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}
position_map_1 = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}

direction_map = {
    "^": (-1, 0),
    "<": (0, -1),
    ">": (0, 1),
    "v": (1, 0),
}


def outer_layer(
        code_from,
        code_to
):
    # HARDCODE
    if code_from == "<":
        if code_to == "<":
            return [""]
        elif code_to == "v":
            return [">"]
        elif code_to == "^":
            return [">^"]
        elif code_to == ">":
            return [">>"]
        elif code_to == "A":
            return [">>^", ">^>"]
    elif code_from == "v":
        if code_to == "<":
            return ["<"]
        elif code_to == "v":
            return [""]
        elif code_to == "^":
            return ["^^"]
        elif code_to == ">":
            return [">"]
        elif code_to == "A":
            return [">^", "^>"]
    elif code_from == ">":
        if code_to == "<":
            return ["<<"]
        elif code_to == "v":
            return ["<"]
        elif code_to == "^":
            return ["<^", "^<"]
        elif code_to == ">":
            return [""]
        elif code_to == "A":
            return ["^"]
    elif code_from == "^":
        if code_to == "<":
            return ["v<"]
        elif code_to == "v":
            return ["v"]
        elif code_to == "^":
            return [""]
        elif code_to == ">":
            return ["v>", ">v"]
        elif code_to == "A":
            return [">"]
    elif code_from == "A":
        if code_to == "<":
            return ["v<<", "<v<"]
        elif code_to == "v":
            return ["v<", "<v"]
        elif code_to == "^":
            return ["<"]
        elif code_to == ">":
            return ["v"]
        elif code_to == "A":
            return [""]


def step(state, key_press):
    # state: up to inner layer (int), robot 1 (str), robot 2 (str)
    output = None
    if key_press == "A":
        if len(state) == 1:
            output = state[0]
        else:
            inner_state, output = step(state[:-1], state[-1])
            state = inner_state + (state[-1],)
    else:
        direction_to_move = direction_map[key_press]
        if len(state) > 1:
            pos_map = position_map_1
        else:
            pos_map = position_map_0

        current_position = pos_map[state[-1]]
        new_position = tuple(c + d for c, d in zip(current_position, direction_to_move))
        new_state = next(k for k, v in pos_map.items() if v == new_position)

        state = state[:-1] + (new_state,)

    return state, output



if __name__ == "__main__":
    sequence = "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"
    state = ("A", "A", "A")
    for s in sequence:
        state, output = step(state, s)
        # print(state)
        if output is not None:
            print(output)