import sys
from functools import cache

import numpy as np
sys.setrecursionlimit(3500)

def parse_input(text):
    points = []
    for line in text.split("\n"):
        if line == "":
            continue
        x, y = line.split(",")
        points.append((int(x), int(y)))
    return points


def generate_grids(points, size=70):
    new_map = np.zeros((size, size), dtype=bool)
    maps = [new_map]
    for point in points:
        new_map = maps[-1].copy()
        new_map[point] = True
        maps.append(new_map)
    return maps


def distance_to_end(
        current_position,
        current_index,
        cache_dict,
        grids,
        increment=False,
):
    key = (current_position, current_index)
    if key in cache_dict:
        return cache_dict[key]

    cache_dict[key] = None

    if current_index == len(grids):
        return None

    current_grid = grids[current_index]
    if current_grid[current_position]:
        return None

    if current_position == tuple(x-1 for x in current_grid.shape):
        cache_dict[key] = 0
        return 0

    neighbour_distances = []
    for direction in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        new_position = (current_position[0] + direction[0], current_position[1] + direction[1])

        if new_position[0] < 0:
            continue

        if new_position[1] < 0:
            continue

        if new_position[0] >= current_grid.shape[0]:
            continue

        if new_position[1] >= current_grid.shape[1]:
            continue

        if increment:
            new_index = current_index + 1
        else:
            new_index = current_index
        distance = distance_to_end(
            new_position,
            new_index,
            cache_dict,
            grids,
            increment=increment
        )
        if distance is not None:
            neighbour_distances.append(distance+1)

    if len(neighbour_distances) == 0:
        return None

    best_distance = min(neighbour_distances)
    cache_dict[key] = best_distance
    return best_distance


def part_one(grid):
    head = [(0, 0)]
    visited = []

    distance_grid = np.zeros_like(grid, dtype=int)

    distance_so_far = 0
    while len(head) > 0:
        # print(len(visited), 71*71 - grid.sum())
        new_head = []
        for h in head:
            visited.append(h)
            distance_grid[h] = distance_so_far
            for direction in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                new_position = (h[0] + direction[0], h[1] + direction[1])
                if new_position in visited or new_position in new_head:
                    continue
                if new_position[0] < 0:
                    continue
                if new_position[1] < 0:
                    continue
                if new_position[0] >= grid.shape[0]:
                    continue
                if new_position[1] >= grid.shape[1]:
                    continue
                if grid[new_position]:
                    continue

                new_head.append(new_position)

        head = new_head
        distance_so_far += 1

    return distance_grid[-1, -1]


if __name__ == "__main__":
    with open("input/day18") as file:
        text = file.read()

#     text = """5,4
# 4,2
# 4,5
# 3,0
# 2,1
# 6,3
# 2,4
# 1,5
# 0,6
# 3,3
# 2,6
# 5,1
# 1,2
# 5,5
# 2,5
# 6,5
# 1,4
# 0,4
# 6,4
# 1,1
# 6,1
# 1,0
# 0,5
# 1,6
# 2,0"""
    grid_size = 71

    points = parse_input(text)
    grids = generate_grids(points, grid_size)

    n_so_far = 1024
    # cache_dict = {}
    # part_one = distance_to_end(
    #     (0, 0),
    #     0,
    #     cache_dict,
    #     grids,
    #     increment=True
    # )
    print(part_one(grids[n_so_far]))

    # for i_grid, grid in enumerate(grids):
    #     if i_grid < 1024:
    #         continue
    #     print(i_grid, part_one(grid))
    # Binary chop: 2862 is not completeable
    print(text.split("\n")[2862-1])