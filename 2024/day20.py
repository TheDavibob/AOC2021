import numpy as np

import common


def solve_maze(maze):
    distance_map = np.zeros_like(maze)
    current_distance = 0
    start_point = tuple(x[0] for x in np.where(maze==2))

    head = [start_point]
    visited = []
    while len(head) > 0:
        new_head = []
        for h in head:
            distance_map[h] = current_distance
            visited.append(h)
            for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_point = tuple(x + y for x, y in zip(h, d))
                if new_point in visited:
                    continue
                if new_point[0] < 0 or new_point[0] >= maze.shape[0]:
                    continue
                if new_point[1] < 0 or new_point[1] >= maze.shape[1]:
                    continue
                if maze[new_point] == 1:
                    continue
                new_head.append(new_point)

        head = new_head
        current_distance += 1

    return distance_map


def analyse_jumps(maze, distance_map):
    savings_map = {}
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == 1:
                continue

            start_distance = distance_map[i, j]
            for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_point = tuple(x + 2*y for x, y in zip((i, j), d))
                if new_point[0] < 0 or new_point[0] >= maze.shape[0]:
                    continue
                if new_point[1] < 0 or new_point[1] >= maze.shape[1]:
                    continue

                end_distance = distance_map[new_point]
                if end_distance > start_distance + 2:
                    savings_map[((i, j), new_point)] = end_distance - start_distance - 2

    return savings_map


def analyse_long_jumps(maze, distance_map, jump_length=20):
    savings_map = {}
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            print(f"Row {i}, Column {j}")
            if maze[i, j] == 1:
                continue

            start_distance = distance_map[i, j]
            for delta_x in range(-20, 21):
                for delta_y in range(-20, 21):
                    if abs(delta_x) + abs(delta_y) > 20:
                        continue
                    new_point = (
                        i + delta_x,
                        j + delta_y
                    )

                    if new_point[0] < 0 or new_point[0] >= maze.shape[0]:
                        continue
                    if new_point[1] < 0 or new_point[1] >= maze.shape[1]:
                        continue

                    end_distance = distance_map[new_point]
                    if end_distance > start_distance + abs(delta_x) + abs(delta_y):
                        savings_map[((i, j), new_point)] = end_distance - start_distance - abs(delta_x) - abs(delta_y)

    return savings_map


if __name__ == "__main__":
    with open("input/day20") as file:
        text = file.read()

#     text = """###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############"""

    maze = common.convert_string_to_np_array(
        text,
        {".": 0,
         "#": 1,
         "S": 2,
         "E": 3}
    )
    distances = solve_maze(maze)
    savings = analyse_jumps(maze, distances)
    print(f"Part 1: {len([v for k, v in savings.items() if v >= 100])}")

    savings = analyse_long_jumps(maze, distances)
    # 2021877 is too high
    # 1948155 is too high
    # 1026965 is too low
    print(f"Part 2: {len([v for k, v in savings.items() if v >= 100])}")