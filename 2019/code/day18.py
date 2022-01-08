from copy import copy
from time import sleep

import numpy as np

import common


def grid_str_to_grid_array(grid_str):
    wall_open_map = {
        ".": 1,
        "#": 0,
        "@": 2
    }
    key_map = {chr(i + 97): i + 100 for i in range(26)}
    door_map = {chr(i + 65): i + 200 for i in range(26)}
    grid_as_array = common.convert_string_to_np_array(grid_str, wall_open_map | key_map | door_map)
    return grid_as_array


def flood_fill(grid_array, source):
    distance = np.inf*np.ones_like(grid_array, dtype=float)
    distance[source] = 0
    current_value = 0

    neighbour_directions = (
        [0, 1],
        [1, 0],
        [-1, 0],
        [0, -1]
    )

    while np.any(np.isinf(distance[grid_array > 0])):
        # Find all edge values
        edge_values = np.where(distance == current_value)
        for i, j in zip(*edge_values):
            for direction in neighbour_directions:
                neighbour_position = tuple(np.array([i, j]) + np.array(direction))
                if grid_array[neighbour_position] == 0:
                    continue
                if not np.isinf(distance[neighbour_position]):
                    continue

                distance[neighbour_position] = current_value + 1

        current_value += 1

    return distance


def get_point_to_point_distance(grid_array, distance, target):
    blockers = []
    total_distance = int(distance[target])
    search_distance = total_distance
    position = target
    while search_distance > 0:
        search_distance -= 1
        directions = (
            [0, 1],
            [1, 0],
            [-1, 0],
            [0, -1]
        )
        for direction in directions:
            neighbour = tuple(np.array(position) + np.array(direction))
            if distance[neighbour] == search_distance:
                position = neighbour
                if grid_array[position] > 2 and (search_distance != 0):
                    blockers.append(grid_array[position])
                break

    return total_distance, blockers[::-1]


def get_distance_graph(grid_array, verbose=True):
    distance_graph = {}
    movement_points = np.where((200 > grid_array) & (grid_array >= 100))

    start_point = np.where((grid_array >= 2) & (grid_array < 100))
    start_value = grid_array[start_point][0]
    start_map = {}
    flood_distance = flood_fill(grid_array, start_point)
    for i, j in zip(*movement_points):
        target = (i, j)
        value = grid_array[i, j]
        start_map[value] = get_point_to_point_distance(grid_array, flood_distance, target)
        if verbose:
            print(f'Added {value} to start key')
    distance_graph[int(start_value)] = start_map

    for k, l in zip(*movement_points):
        source_value = grid_array[k, l]
        flood_distance = flood_fill(grid_array, (k, l))
        new_map = {}
        for i, j in zip(*movement_points):
            if (i == k) and (j == l):
                continue

            target = (i, j)
            value = grid_array[i, j]

            if distance_graph.get(value, None) is not None:
                distance, blockers = distance_graph[value][source_value]
                new_map[value] = (distance, blockers[::-1])
            else:
                new_map[value] = get_point_to_point_distance(grid_array, flood_distance, target)
            if verbose:
                print(f'Added {value} to {source_value}')
        distance_graph[source_value] = new_map

    return distance_graph


def get_viable_points(distance_graph, current_value, keys_so_far):
    viable_targets = []
    for possible_target, (distance, blockers) in distance_graph[current_value].items():
        if possible_target in keys_so_far:
            continue

        is_viable = True
        for s in blockers:
            if (s not in keys_so_far) and (s-100 not in keys_so_far):
                is_viable = False
                break

        if is_viable:
            viable_targets.append((possible_target, distance))

    return viable_targets


def search_on_grid_str(grid_str, verbose=True):
    grid_array = grid_str_to_grid_array(grid_str)
    distance_graph = get_distance_graph(grid_array, verbose)
    return recurse_search(distance_graph, 2, [2], {})


def recurse_search(distance_graph, current_position, history, state_history):
    state = (current_position, tuple(sorted(history)))
    if state in state_history.keys():
        return state_history[state]

    is_finished = True
    for source in distance_graph.keys():
        if source not in history + [current_position]:
            is_finished = False
            break

    if is_finished:
        return 0

    viable_targets = get_viable_points(distance_graph, current_position, history + [current_position])
    best_outcome = None

    for target, distance in viable_targets:
        next_step = recurse_search(distance_graph, target, sorted(history + [current_position]), state_history)
        if next_step is None:
            continue

        outcome = distance + next_step
        if (best_outcome is None) or (outcome < best_outcome):
            best_outcome = outcome

    state_history[state] = best_outcome
    return best_outcome


def chop_up_grid_array(grid_array, deal_with_middle = True):
    middle = ((grid_array.shape[0] + 1) // 2, (grid_array.shape[1] + 1) // 2)
    if deal_with_middle:
        grid_array[middle[0]-2:middle[0]+1, middle[0]-2:middle[0]+1] = np.array([[2, 0, 2], [0, 0, 0], [2, 0, 2]])

    grid_array[grid_array == 2] = [2, 3, 4, 5]

    grid_0 = grid_array[:middle[0], :middle[1]]
    grid_1 = grid_array[:middle[0], middle[1]-1:]
    grid_2 = grid_array[middle[0]-1:, :middle[1]]
    grid_3 = grid_array[middle[0]-1:, middle[1]-1:]
    return grid_0, grid_1, grid_2, grid_3


def recurse_search_multi(distance_graphs, current_positions, history, state_history):
    state = (current_positions, tuple(history))
    if state in state_history.keys():
        return state_history[state]

    all_sources = []
    for distance_graph in distance_graphs:
        for source in distance_graph.keys():
            all_sources.append(source)

    is_finished = True
    for source in all_sources:
        if source not in history.union(set(current_positions)):
            is_finished = False

    if is_finished:
        return 0

    viable_targets = {}
    for i, (distance_graph, current_position) in enumerate(zip(distance_graphs, current_positions)):
        viable_targets[i] = get_viable_points(distance_graph, current_position, {*history, *current_positions})

    best_outcome = None
    for i in range(4):
        for target, distance in viable_targets[i]:
            full_targets = list(current_positions)
            current_position = full_targets[i]
            full_targets[i] = target
            next_step = recurse_search_multi(distance_graphs, tuple(full_targets), {*history, current_position}, state_history)
            if next_step is None:
                continue

            outcome = distance + next_step
            if (best_outcome is None) or (outcome < best_outcome):
                best_outcome = outcome

    state_history[state] = best_outcome
    return best_outcome


def part_2(grid_str, sort_out_middle=True, verbose=True):
    grid_array = grid_str_to_grid_array(grid_str)
    grid_arrays = chop_up_grid_array(grid_array, sort_out_middle)

    distance_graphs = []
    for g in grid_arrays:
        distance_graphs.append(get_distance_graph(g, verbose))

    answer = recurse_search_multi(distance_graphs, (2, 3, 4, 5), {2, 3, 4, 5}, {})
    return answer


if __name__ == "__main__":
    grid_str = """#################################################################################
#..........c#.............E.......#.....#.....#...#.........#...#...............#
#.#########.#.#.#################.#.#####.#.#.#.#.#.#######.#.#.#.#########.#####
#.#...R...#.#.#.#.#.....#.....#.#.#....t#.#.#.#.#.#.#.....#...#...#.......#.....#
###.#####.#.#G#.#.#.#.###.#.#.#.#.#####.###.###.#.#.###.#.###############.#####.#
#...#.....#...#.#...#.....#.#...#.....#.#...#...#.#...#.#p........#...........#.#
#.#####.#######.#####.#####.#########V#.#.###.###.###.#.#######.#.#.#####.#####.#
#.#...#.....#...#...#.....#...#...#...#.#...#...#...#.#.#.....#.#.#.....#.#.....#
#.#.#W#####.#.###.#.#########.#.#.#.###.#.#.###.###.#.###.###.#.#.#.###.###.###.#
#...#.#.#...#.#...#.....#.....#.#...#...#.#...#.#.#.#...#.#...#.#.#...#.#...#.#.#
#####.#.#.###.#.#.#####.#.#.###.#####.###.#.#.#.#.#.###.#.#.###.#.#####.#.###.#.#
#.....#.#...#.#d#.#...#o#.#.#...#.#.....#.#.#.#.#.#...#j#.#x#...#.......#.#.#...#
#.#####.###.#.#.###.#.#.#.###.###.#.###.#.#.#.#.#.###.#.#.#.#.###.#####.#.#.#.###
#.....#...#...#.....#.#.#...#.#.....#...#.#.#.#.....#.#...#...#...#...#.#.#.#.#.#
#.###.###.###.#######.#.#.#.#.#####.#.###.#.#######.#.#####.#####.#.#.###.#.#.#.#
#.#.#...#.....#...#...#.#.#.#.....#.#...#.#.#.......#...#...#...#.#.#.....#.#.#.#
#.#A###.#.#######.#.###Q###.#####.#####.#.#.#.#######.###.###.#.###.#######.#.#.#
#.#...#.#.........#...#...#...#...#.....#.#.........#.....#.#.#...#.#.......#w#.#
#.#.#.#.#########.###.###.###.#.###.###.#####.###########.#.#.###.#.#####.#.#.#.#
#...#.#...#.......#..s#.....#.#...#.#.#.#...#.#.........#...#.#...#.#...#.#...#.#
###.#####.#########.#######.#.###.#.#.#.#.#.#.#.#######.###.#.#.###.#.#.###.###.#
#...#...#.......#...#...#...#...#...#...#.#.#.#.#...#...#...#.#...#...#...#.....#
#.###.#.#######.#.#.###.#.#####.#####.###.#.###.#.#.#.#.#########.#.#####.#####.#
#n..#.#.......#.#.#...#.#.....#.....#...#.#.....#.#.#.#.#.....#...#.....#.....#a#
###.#.#######.#.#.#####.#####.#.###.###.#.#######.#.#.#.#.#.###.#######.#####.#.#
#...#.#.....#...#.....#.#...#.#...#...#.#.#.....#.#...#.#.#.#...#.....#.....#.#.#
#.###.#.###.#########.#K#.###B###.#####.#.#.###.#.#######.#.#.#####.#.#####.#.#.#
#.#.#.....#.#.......#...#...#...#...#...#.#...#.#.....#...#...#...#.#...#...#.#.#
#.#.#######.#.#####.#######.###.###.#.###.###.#.#####.#.#######.#.#.#.###.###.#.#
#...#...#...#...#i#...#.......#...#.....#.#...#.#...#...#.....#.#.#.#.#...#.#.#.#
###.#.###.#####.#.#.###.#.#######.#####.#.#.#####.#.#####.###.#.#.#.#.#.###.#.#.#
#...#.#...#.....#.#...#.#.......#...#...#.#.......#.....#...#...#.#.#.......#.#.#
#.###.#.#.#.#####.###.#.#######.###.#.###.#######.###.#.###.#####.###.#######.###
#.#...#.#.#.#.....#...#...#.#...#...#...#...#...#...#.#.....#...#...#.#.....#...#
#.###.#.###.#.###.#.#.###.#.#.###.#####.###.#.#.###.#.#######.#.###.###.###.###.#
#...#.#.#...#..z#.#.#...#.#.#...#.#.....#...#.#.#...#.....#.#.#...#.....#.#...#.#
###.#.#.#.###.#.#.#.#####.#.###.#.#.#####.###.#.#########.#.#.###.#######.###.#.#
#.#...#.#...#.#.#.#.......#...#...#...#.#.....#.........#.#.#.#...#.......#...#.#
#.###.#.###.#.#.###########.#.#######.#.###############.#.#.#.#.###.#.#####.###.#
#.....#.....#.#.......H.....#........................h....#...#.....#...........#
#######################################.@.#######################################
#....m....#.#.........#.....#.............#...#...............#.........#.......#
#.#.#####.#.#.#######.#.#####.###.#####.#.#.#.#.#.#.###########.#####.#.#.#.#####
#.#.#.....#.#...#...#.#.#.....#.#.#...#.#.#.#...#.#.#.....#.....#.I...#...#.#...#
#.#.###.###.###.#.#.#.#.#.#####.#.#.#.#.#.#.#####.###.###.#.#####.#####.#####.#.#
#.#...#.......#.#.#...#.#.......#.#.#.#.#...#...#.......#...#.....#...#.#.....#.#
#.###.#######.#.#.#####.#######.#.#.#.#.#####.#.#######.#####.#####.###.#.#####.#
#...#.....#...#.#.#.......#.....#...#.#.#.....#.....#.#.#...#.....#.....#.#....b#
#.#######.#.###.#.#######.#.#########.###.#########.#.#.###.#####.#.#####.#.#####
#.#.......#u..#.#.......#.#...#.#...#...#.#...#.#...#.......Z.#...#...#q..#.#...#
###.###########.#######.#.###.#.#.#.#.#.#.#.#.#.#.###.#########.#######.###.#.#.#
#...#.L.......#...#...#.#...#...#.#.#.#.#...#.#.#.#...#.........#.......#...#.#.#
#.###.#######.###.###.#.#.#.#.###.#.###.#####.#.#.#.###.#####.###.#######U#####.#
#y....#.....#...#.....#.#.#...#...#.....#.....#.#.#...#...#.#.#...#.....#.......#
#.#####.#######.#####.#.#######.#######.#.#####.#.#######.#.#.#.#####.#########.#
#.#..f..#.......#.....#...#.....#.....#.#...#.......#.....#...#.#...#.#.......#.#
#.#.#####.#####.#.#######.#.#####.###.#.#.#.#######.#.#######.#.#.#.#M#.###.###.#
#.#.#...#.....#.#...#.....#...#.....#.#.#.#.....#.#.#.#.....#.#.#.#...#...#.....#
#.#.#.#.#.###.#.###.#.#####.#.#####.###.#######.#.#.#.#.###.###.#.#.#####.#######
#...#.#.#...#.#...#.#.#...#.#.....#.#...#.......#.#...#.#.#.....#.#.#.F...#.....#
#####.#.###.#.#####.#.#.###.#####.#.#.###.#######.#.###.#.#.#####.###.#######.#Y#
#.....#...#.#.....#.#.#...#.....#.#.#...#.....#...#.#...#.#.#.#.......#.......#.#
#.#######.#######.#.###.#.###.###.#.###.#.###.#.###.#.###.#.#.#######.###.#####.#
#.#...............#...#.#.#...#...#.....#...#.#.#...#.#...O.#.......#.....#.....#
#.#############.#####.#.#.#.###.###.#######.#.#.#.###D#############.#######.#####
#.........#...#.#...#.#.#...#.#.#.#.#...#...#.#.#...#.....#.......#...#...#.....#
#########.#.#.###.#.#.#.#####.#.#.#.#.#######.#C###.#####.#.#.#######.###.#####.#
#.....#...#.#...#r#.#.#.......#.#.#.#...#.....#...#.#...#...#.S.#..k..#.....#...#
#.###.#.#.#.###.#.#.#.#########.#.#.#.#.#.#####.#.#.###.#######.#.#####.#####.###
#.#.#.#.#.#.#.#...#.#.#...#...#.#...#.#.#.#.....#.#.....#.....#...#...........#.#
#.#.#.#.#.#.#.#####.#.#.#.#.#.#.#.#####.#.#.#.#####.#####.###.#####.###########.#
#.#.....#.#...#.#...#.#.#.#.#v..#.......#.#.#.#.....#...#...#.#...#...#.......#.#
#.###########.#.#.#.#.#.#.#.###########.#.###.#.#####.#.###.#.#.#.###.#.#.###.#P#
#...............#.#.#..e#...#...#.T.....#...#.#.#.....#...#.#...#.....#.#.#l#...#
#.###############.#.#########.###.#######.#.#.#.#.#######.#.###########.#.#.###.#
#.#.........#.....#.#...#.......#.#.....#.#.#...#.#.....#...#.J...#...#.#.#.....#
#.#######.#.#.#######.#.#.#####.#.#.###.#.#.#####.#.###.#####.###.###.#.#.###.###
#.........#.#.....#...#.#.....#...#.#.#.#.#.#.....#.#.........#.#...#...#.X.#...#
###########.#####.#.###.#####.#####.#.#.#.#.#.#######.#########.###.#######.###.#
#...............#.....#.............#..g#.#.......N...#.....................#...#
#################################################################################
"""
    common.part(1, search_on_grid_str(grid_str))
    common.part(2, part_2(grid_str, sort_out_middle=True))