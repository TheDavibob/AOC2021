import functools

from tqdm import tqdm

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


def make_adjacency_map(n_levels):
    # Output only written in state (output, A, A) so it's fundamentally just finding all the paths that do this
    # traversal
    # What states are "next to" each other?
    states = [
        (x, y, z)
        for x in position_map_0.keys()
        for y in position_map_1.keys()
        for z in position_map_1.keys()
    ]

    adjacency_map = {}
    for state in states:
        adjacent_states = []
        for direction in "^<v>A":
            try:
                new_state, output = step(state, direction)
                adjacent_states.append(new_state)
            except StopIteration:
                pass
        adjacency_map[state] = adjacent_states

    return states, adjacency_map


def dijkstra_simple(state_from, adjacency_map):
    head = [state_from]
    distance_map = {}
    visited_states = []
    current_distance = 0
    while len(head) > 0:
        new_head = []
        for h in head:
            visited_states.append(h)
            distance_map[h] = current_distance
            for neighbour in adjacency_map[h]:
                if neighbour in visited_states:
                    continue
                new_head.append(neighbour)
        head = new_head
        current_distance += 1

    return distance_map


def find_all_shortest_paths(from_state, to_state, distance_map, adjacency_map):
    distance_to_target = distance_map[from_state][to_state]
    target_distance = distance_to_target - 1
    paths = [(to_state,)]
    while target_distance >= 0:
        new_paths = []
        for p in paths:
            head = p[-1]
            for neighbour in adjacency_map[head]:
                if distance_map[from_state][neighbour] == target_distance:
                    new_paths.append(tuple(s for s in p) + (neighbour,))

        paths = new_paths
        target_distance -= 1

    return paths


def run(sequences, n_levels=2):
    states, adj_map = make_adjacency_map(n_levels)
    distance_map = {}
    for k in tqdm(position_map_0.keys()):
        state = (k, "A", "A")
        distance_map[state] = dijkstra_simple(state, adj_map)

    # paths = find_all_shortest_paths(("A", "A", "A"), ("A", "A", "<"), distance_map, adj_map)

    state_distances = {}
    for k in tqdm(position_map_0.keys()):
        for l in position_map_0.keys():
            state_distances[(k, l)] = distance_map[(k, "A", "A")][(l, "A", "A")]

    total_val = 0
    for sequence in sequences:
        shorted_distance = 0
        long_sequence = "A" + sequence
        for f, t in zip(long_sequence[:-1], long_sequence[1:]):
            shorted_distance += state_distances[(f, t)] + 1
        val = shorted_distance*int(sequence[:-1])
        print(shorted_distance, int(sequence[:-1]), val)
        total_val += val

    return total_val


if __name__ == "__main__":
    # test input
#     text = """029A
# 980A
# 179A
# 456A
# 379A"""

    text = """540A
582A
169A
593A
579A"""

    sequences = text.split("\n")
    total_val = run(sequences)

    # sequence = "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"
    # state = ("A", "A", "A")
    # for s in sequence:
    #     state, output = step(state, s)
    #     print(state)
    #     if output is not None:
    #         print(output)

    print(f"Part 1: {total_val}")