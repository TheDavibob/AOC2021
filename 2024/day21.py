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


def make_layer_adj_map(position_map):
    states = list(position_map.keys())
    adjacency_map = {}
    for state in states:
        current_position = position_map[state]
        neighbours = []
        for direction in "^<v>":
            direction_to_move = direction_map[direction]
            new_position = tuple(c + d for c, d in zip(current_position, direction_to_move))
            try:
                new_state = next(k for k, v in position_map.items() if v == new_position)
                neighbours.append(new_state)
            except StopIteration:
                pass
        adjacency_map[state] = neighbours

    return adjacency_map



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


def find_paths(from_state, to_state, adjacency_map, position_map):
    paths = [(from_state,)]
    completed_paths = []
    while len(paths) > 0:
        new_paths = []
        for path in paths:
            head = path[-1]
            neighbours = adjacency_map[head]
            for neighbour in neighbours:
                if neighbour == to_state:
                    completed_paths.append(path + (neighbour,))
                elif neighbour in path:
                    continue
                else:
                    new_paths.append(path + (neighbour,))

        paths = new_paths

    completed_as_directions = []
    for path in completed_paths:
        as_directions = ""
        for s_f, s_t in zip(path[:-1], path[1:]):
            pos_f = position_map[s_f]
            pos_t = position_map[s_t]
            pos_delta = tuple(x - y for x, y in zip(pos_t, pos_f))
            direction = next(k for k, v in direction_map.items() if v==pos_delta)
            as_directions += direction
        completed_as_directions.append(as_directions)
    return completed_as_directions


def find_all_paths(position_map):
    adjacency_map = make_layer_adj_map(position_map)
    states = list(adjacency_map.keys())
    paths = {}
    for s_f in states:
        for s_t in states:
            if s_t == s_f:
                paths[(s_f, s_t)] = [""]
            else:
                paths[(s_f, s_t)] = find_paths(s_f, s_t, adjacency_map, position_map)

    return paths


def find_best_paths(paths, cost_lookup):
    # The layer above defines the cost of each movement. Use this to find the cost of each path
    paths_cost = {}
    for state_pair, each_paths in paths.items():
        best_cost = None
        for path in each_paths:
            cost = 0
            for s_f, s_t in zip("A" + path, path + "A"):
                cost += cost_lookup[(s_f, s_t)]
            if best_cost is None:
                best_cost = cost
            elif cost < best_cost:
                best_cost = cost
        paths_cost[state_pair] = best_cost
    return paths_cost


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
    # total_val = run(sequences)
    # print(f"Part 1: {total_val}")

    # sequence = "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"
    # state = ("A", "A", "A")
    # for s in sequence:
    #     state, output = step(state, s)
    #     print(state)
    #     if output is not None:
    #         print(output)
    paths_1 = find_all_paths(position_map_1)
    paths_0 = find_all_paths(position_map_0)

    upper_cost_lookup = {(x, y): 1 for x in "^<v>A" for y in "^>v<A"}
    next_cost_lookup = upper_cost_lookup
    n_layers = 25
    for _ in range(n_layers):
        next_cost_lookup = find_best_paths(paths_1, next_cost_lookup)

    final_cost_lookup = find_best_paths(paths_0, next_cost_lookup)
    total_val = 0
    for path in sequences:
        cost = -1  # Ignore the first A
        for s_f, s_t in zip("A" + path, path + "A"):
            cost += final_cost_lookup[(s_f, s_t)]
        val = cost*int(path[:-1])
        print(cost, int(path[:-1]), val)
        total_val += val
    print(f"Part 2: {total_val}")  # Part 1 can do this to with n_iterations = 2
