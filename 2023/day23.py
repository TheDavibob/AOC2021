import sys

import numpy as np
from tqdm import tqdm

import common

sys.setrecursionlimit(10000)


def parse_input(text):
    return common.convert_string_to_np_array(
        text,
        {".": 0, "#": 1, ">": 2, "v": 3}
    ).astype(int)


def longest_path(from_point, points_so_far, grid, target_point=None, break_early=False):
    if target_point is None:
        if from_point[0] == grid.shape[0]-1:
            return 0
    elif from_point == target_point:
        return 0

    head = []
    for test_dir in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        test_point = (from_point[0] + test_dir[0], from_point[1] + test_dir[1])
        if grid[test_point] == 1:
            continue
        elif grid[test_point] == 2:
            if test_dir != (0, 1):
                continue
        elif grid[test_point] == 3:
            if test_dir != (1, 0):
                continue
        elif test_point in points_so_far:
            continue

        head.append(test_point)

    if not head:
        return None

    best_so_far = None
    for test_point in head:
        best_length = longest_path(test_point, points_so_far + [from_point], grid)

        if best_length is not None:
            if break_early:
                return best_length + 1

            new_length = best_length + 1
            if best_so_far is None:
                best_so_far = new_length
            elif best_length > best_so_far:
                best_so_far = new_length

    return best_so_far


def find_branch_points(grid):
    three_ways = []
    four_ways = []

    for i_row in range(1, grid.shape[0]-1):
        for i_col in range(1, grid.shape[1]-1):
            from_point = (i_row, i_col)
            if grid[from_point] == 1:
                continue
            neighbours = 0
            for test_dir in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                test_point = (from_point[0] + test_dir[0], from_point[1] + test_dir[1])
                if grid[test_point] == 0:
                    neighbours += 1

            if neighbours == 3:
                three_ways.append(from_point)
            elif neighbours == 4:
                four_ways.append(from_point)

    return three_ways, four_ways


def find_longest_path(graph_representation, current_node, nodes_visited, target_node, cache_dict):
    if current_node == target_node:
        return 0

    cached = cache_dict.get((current_node, tuple(sorted(nodes_visited))), "null")
    if cached != "null":
        return cached

    best_distance = None
    for neighbour, distance in graph_representation[current_node].items():
        if neighbour in nodes_visited:
            continue
        distance_from_neighbour = find_longest_path(
            graph_representation,
            neighbour,
            nodes_visited + [current_node],
            target_node,
            cache_dict
        )
        if distance_from_neighbour is not None:
            if best_distance is None:
                best_distance = distance_from_neighbour + distance
            else:
                best_distance = max(best_distance, distance_from_neighbour + distance)

    cache_dict[(current_node, tuple(sorted(nodes_visited)))] = best_distance
    return best_distance


def part_one(grid):
    start_point = np.where(grid[0]==0)
    start_point = (0, start_point[0][0])
    return longest_path(start_point, [], grid)


def part_two(grid):
    graph_network, sources = reduced_network(grid == 1)
    return find_longest_path(graph_network, sources[0], [], sources[1], {})



def steps_in_direction(from_point, initial_direction, grid, targets):
    to_point = from_point[0] + initial_direction[0], from_point[1] + initial_direction[1]

    if grid[to_point]:
        return None

    n_steps = 1
    if to_point in targets:
        return n_steps, to_point

    prev_direction = initial_direction

    while True:
        for next_direction in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            if prev_direction[0] == -next_direction[0] and prev_direction[1] == -next_direction[1]:
                continue

            new_target = to_point[0] + next_direction[0], to_point[1] + next_direction[1]
            if grid[new_target] == 0:
                to_point = new_target
                n_steps += 1
                prev_direction = next_direction
                break

        if grid[new_target] != 0:
            raise ValueError("Can't move")

        if to_point in targets:
            return n_steps, to_point


def reduced_network(grid):
    threes, fours = find_branch_points(grid==1)

    print("Found all nodes")

    start_point = np.where(grid[0]==0)
    start_point = (0, start_point[0][0])

    end_line = grid.shape[0]-1
    end_point = np.where(grid[end_line]==0)
    end_point = (end_line, end_point[0][0])
    sources = [start_point, end_point]

    network_grid = {}
    all_nodes = sources + threes + fours
    for node in threes + fours:
        node_connections = {}
        for next_direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            output = steps_in_direction(node, next_direction, grid == 1, all_nodes)
            if output is not None:
                node_connections[output[1]] = output[0]
                if output[1] in sources:
                    network_grid[output[1]] = {node: output[0]}

        network_grid[node] = node_connections

    print("Made network grid")

    return network_grid, sources



if __name__ == "__main__":
    text = common.import_file("input/day23")
    test_text = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

    grid = parse_input(text)
    demo_grid = parse_input(test_text)

    assert part_one(demo_grid) == 94
    assert part_two(demo_grid) == 154

    # common.part(1, part_one(grid))
    common.part(2, part_two(grid))

    # TODO:
    #  - Find pairwise difference between all "nodes", that is junctions. Probably only need the closest set of nodes.
    #  - This should be OK: for each node, go in a valid direction and follow until find another node. Nothing
    #    complicated needed.
    #  - Then do the recursion on this much reduced space of nodes->nodes and distances.
