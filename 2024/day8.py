import numpy as np

import common


def parse_input(text):
    return common.convert_string_to_np_array(
        text,
        mapping_dict={".": 0}
    )


def find_all_antinodes(node_map, part=1):
    if part == 1:
        finder = find_antinodes
    else:
        finder = find_antinodes_2

    unique_nodes = [node for node in np.unique(node_map) if node != 0]
    one_hot_map = np.zeros(node_map.shape + (len(unique_nodes),), dtype=bool)
    for node in unique_nodes:
        one_hot_map[..., unique_nodes.index(node)] = finder(node_map, node)

    return one_hot_map


def find_antinodes(node_map, node_id):
    nodes = np.where(node_map == node_id)

    antinode_map = np.zeros(node_map.shape, dtype=bool)
    def add_to_antinode_map(index):
        if index[0] < 0:
            return
        if index[1] < 0:
            return

        if index[0] >= antinode_map.shape[0]:
            return
        if index[1] >= antinode_map.shape[1]:
            return

        antinode_map[index[0], index[1]] = True

    node_xy = [(i, j) for (i, j) in zip(*nodes)]
    for i_node, node in enumerate(node_xy):
        for other_node in node_xy[i_node+1:]:
            node_0 = np.array(node)
            node_1 = np.array(other_node)

            node_delta = node_0 - node_1
            antinode_0 = node_0 + node_delta
            antinode_1 = node_1 - node_delta

            add_to_antinode_map(antinode_0)
            add_to_antinode_map(antinode_1)

    return antinode_map


def find_antinodes_2(node_map, node_id):
    nodes = np.where(node_map == node_id)

    antinode_map = np.zeros(node_map.shape, dtype=bool)
    def add_to_antinode_map(index):
        if index[0] < 0:
            return
        if index[1] < 0:
            return

        if index[0] >= antinode_map.shape[0]:
            return
        if index[1] >= antinode_map.shape[1]:
            return

        antinode_map[index[0], index[1]] = True

    node_xy = [(i, j) for (i, j) in zip(*nodes)]
    for i_node, node in enumerate(node_xy):
        for other_node in node_xy[i_node+1:]:
            node_0 = np.array(node)
            node_1 = np.array(other_node)

            node_delta = node_0 - node_1

            node_delta //= np.gcd(*node_delta)

            max_steps = node_map.shape[0] // (np.max(np.abs(node_delta)) - 1)

            for step in range(-max_steps, max_steps):
                add_to_antinode_map(node_0 + step * node_delta)

    return antinode_map


if __name__ == "__main__":
    with open("input/day8") as file:
        text = file.read()

    node_map = parse_input(text)
    antinodes = find_all_antinodes(
        node_map,
        part=1
    )
    print(f"Part 1: {np.sum(np.any(antinodes, axis=-1))}")

    antinodes = find_all_antinodes(
        node_map,
        part=2
    )
    print(f"Part 2: {np.sum(np.any(antinodes, axis=-1))}")