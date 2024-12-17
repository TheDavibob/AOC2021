import json
import sys

import numpy as np

import common

sys.setrecursionlimit(2500)

DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]
DIRECTION_MAP = {
    (1, 0): 2,
    (0, 1): 1,
    (-1, 0): 3,
    (0, -1): 0,
}


def parse_input(text):
    return common.convert_string_to_np_array(
        text,
        {".": 0, "#": 1, "S": 2, "E": 3}
    )


def step(
        current_location,
        current_direction,
        cache_dict,
        maze,
):
    print(current_location, current_direction)
    key = (current_location, current_direction)
    if key in cache_dict.keys():
        return cache_dict[key]

    cache_dict[key] = None  # Placeholder - if we come back here before we've figured it out, ignore

    if maze[current_location] == 1:
        cache_dict[key] = None
        return None

    if maze[current_location] == 3:
        score = 0
        cache_dict[key] = score
        return score

    scores = []
    score = step(
        (current_location[0] + current_direction[0], current_location[1] + current_direction[1]),
        current_direction,
        cache_dict=cache_dict,
        maze=maze,
    )
    if score is not None:
        scores.append(score + 1)

    for direction in DIRECTIONS:
        if direction == current_direction:
            continue

        score = step(
            current_location,
            direction,
            cache_dict=cache_dict,
            maze=maze,
        )
        if score is not None:
            scores.append(score + 1000)

    if len(scores) == 0:
        cache_dict[key] = None
        return None

    best_score = min(scores)
    cache_dict[key] = best_score
    return best_score


def branching_search(
        start_point,
        start_direction,
        maze
):
    distance_from_start = {}
    unvisited_set = []
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == 1:
                continue
            for direction in DIRECTIONS:
                distance_from_start[((i, j), direction)] = float("inf")
                unvisited_set.append(((i, j), direction))

    distance_from_start[(start_point, start_direction)] = 0
    while len(unvisited_set) > 0:
        print(f"Left to visit: {len(unvisited_set)}")
        potential_nodes = [
            node for node in unvisited_set if distance_from_start[node] < float("inf")
        ]

        best_score = float("inf")
        best_node = None
        for node in potential_nodes:
            if distance_from_start[node] < best_score:
                best_score = distance_from_start[node]
                best_node = node

        unvisited_set.remove(best_node)

        neighbours = []
        node_loc, node_direction = best_node
        for direction in DIRECTIONS:
            if direction == node_direction:
                new_loc = (node_loc[0] + direction[0], node_loc[1] + direction[1])
                if maze[new_loc] == 1:
                    continue

                neighbours.append((new_loc, direction))
            else:
                neighbours.append((node_loc, direction))

        node_score = distance_from_start[best_node]
        for neighbour in neighbours:
            current_score = distance_from_start[neighbour]
            if neighbour[1] == node_direction:
                if node_score + 1 < current_score:
                    distance_from_start[neighbour] = node_score + 1

            else:
                if node_score + 1000 < current_score:
                    distance_from_start[neighbour] = node_score + 1000

    return distance_from_start


def find_optimal_neighbours(
        point_from,
        direction_from,
        distance_from_start,
):
    neighbours = []
    current_score = distance_from_start[(point_from, direction_from)]
    for direction in DIRECTIONS:
        if direction == direction_from:
            new_loc = (point_from[0] - direction[0], point_from[1] - direction[1])
            if (new_loc, direction) not in distance_from_start:
                continue

            if distance_from_start[(new_loc, direction)] == current_score - 1:
                neighbours.append((new_loc, direction))
        else:
            if (point_from, direction) not in distance_from_start:
                continue
            if distance_from_start[(point_from, direction)] == current_score - 1000:
                neighbours.append((point_from, direction))

    return neighbours


def find_all_points_on_optimal_paths(
        distance_from_start,
        end_point,
):
    end_points_in_dict = {
        k: v for k, v in distance_from_start.items()
        if k[0] == end_point
    }
    best_end_points = [
        k for k, v in end_points_in_dict.items()
        if v == min(end_points_in_dict.values())
    ]

    points_so_far = [x for x in best_end_points]
    head = [x for x in best_end_points]
    while len(head) > 0:
        print(head)
        test_head = head.pop()
        # head.remove(test_head)
        neighbours = find_optimal_neighbours(
            test_head[0],
            test_head[1],
            distance_from_start
        )
        head.extend(neighbours)
        points_so_far.extend(neighbours)

    return points_so_far




if __name__ == "__main__":
    with open("input/day16") as file:
        text = file.read()

#     text = """###############
# #.......#....E#
# #.#.###.#.###.#
# #.....#.#...#.#
# #.###.#####.#.#
# #.#.#.......#.#
# #.#.#####.###.#
# #...........#.#
# ###.#.#####.#.#
# #...#.....#.#.#
# #.#.#.###.#.#.#
# #.....#...#.#.#
# #.###.#.#.#.#.#
# #S..#.....#...#
# ###############"""

    start_map = parse_input(text)

    start_point = np.where(start_map == 2)
    # cache_dict = {}
    # score = step(
    #     (start_point[0][0], start_point[1][0]),
    #     current_direction=(0, 1),
    #     maze=start_map,
    #     cache_dict=cache_dict
    # )
    # print(f"Part 1: {score}")  # Doesn't work: recursion crashes everything

    # distance_from_start = branching_search(
    #     (start_point[0][0], start_point[1][0]),
    #     start_direction=(0, 1),
    #     maze=start_map
    # )
    # end_point = np.where(start_map == 3)
    # print(
    #     "Part 1:",
    #     min([distance_from_start[((end_point[0][0], end_point[1][0]), d)] for d in DIRECTIONS])
    # )
    #
    # # Part 2: back out from distance_from_start the best paths, by starting at the end and finding points
    # # which are the "correct" distance away
    # distance_from_start_as_list = [
    #     k + (v,)
    #     for k, v in distance_from_start.items()
    # ]
    # with open("Day16Part1.json", "w+") as file:
    #     json.dump(distance_from_start_as_list, file, indent=4)

    with open("Day16Part1.json", "r") as file:
        distance_from_start_as_list = json.load(file)

    distance_from_start = {}
    for loc, dir, val in distance_from_start_as_list:
        distance_from_start[(tuple(loc), tuple(dir))] = val

    end_point = np.where(start_map == 3)
    end_point = (end_point[0][0], end_point[1][0])

    all_points_locs = find_all_points_on_optimal_paths(distance_from_start, end_point)
    print(f"Part 2: {len(set(k[0] for k in all_points_locs))}")
