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


def find_node_to_node_distance(sources, three_points, four_points, grid):
    all_nodes = sources + three_points + four_points
    distance_array = -1 * np.ones((len(all_nodes), len(all_nodes)), dtype=int)

    filled_grid = (grid == 1).astype(int)
    for node in all_nodes:
        filled_grid[node] = 1

    print("Threes:", len(three_points))
    print("Fours:", len(four_points))

    for i_from, from_node in tqdm(enumerate(three_points)):
        if np.sum(distance_array[len(sources) + i_from] > 0) == 3:
            continue
        for i_to, to_node in enumerate(all_nodes):
            if to_node == from_node:
                continue
            distance = find_pairwise_distance(from_node, to_node, filled_grid)
            if distance is not None:
                distance_array[len(sources) + i_from, i_to] = distance

    for i_from, from_node in tqdm(enumerate(four_points)):
        if np.sum(distance_array[len(sources) + len(three_points) + i_from] > 0) == 4:
            continue
        for i_to, to_node in enumerate(all_nodes):
            if to_node == from_node:
                continue
            distance = find_pairwise_distance(from_node, to_node, filled_grid)
            if distance is not None:
                distance_array[len(sources) + len(three_points) + i_from, i_to] = distance

    return distance_array


def find_longest_path(distance_grid, current_node, nodes_visited, target_node):
    # start at node 0, aiming for node 1
    if current_node == target_node:
        return 0

    target_nodes = np.where(distance_grid[0])


def find_pairwise_distance(from_point, to_point, filled_grid):
    new_grid = filled_grid.copy()
    new_grid[from_point] = 0
    new_grid[to_point] = 0
    distance = longest_path(from_point, [], new_grid, to_point)

    return distance



def part_one(grid):
    start_point = np.where(grid[0]==0)
    start_point = (0, start_point[0][0])
    common.part(1, longest_path(start_point, [], grid))


def part_two(grid):
    grid = (grid == 1)

    start_point = np.where(grid[0]==0)
    start_point = (0, start_point[0][0])
    common.part(2, longest_path(start_point, [], grid))


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

    # part_one(grid)
    # part_two(grid)

    grid = demo_grid
    threes, fours = find_branch_points(grid==1)

    start_point = np.where(grid[0]==0)
    start_point = (0, start_point[0][0])

    end_line = grid.shape[0]-1
    end_point = np.where(grid[end_line]==0)
    end_point = (end_line, end_point[0][0])
    sources = [start_point, end_point]

    # d = find_node_to_node_distance(sources, threes, fours, grid)

    # TODO:
    #  - Find pairwise difference between all "nodes", that is junctions. Probably only need the closest set of nodes.
    #  - This should be OK: for each node, go in a valid direction and follow until find another node. Nothing
    #    complicated needed.
    #  - Then do the recursion on this much reduced space of nodes->nodes and distances.

    all_nodes = sources + threes + fours
    for next_direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        print(steps_in_direction(all_nodes[3], next_direction, grid==1, all_nodes))