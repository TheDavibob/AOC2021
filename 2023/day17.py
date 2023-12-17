import functools
from collections import deque

import numpy as np
from tqdm import tqdm

import common


def parse_input(text):
    return common.convert_string_to_np_array(
        text,
        {str(i): i for i in range(10)}
    )


# Grid approach - the one above didn't work
DIRECTIONS = ["U", "D", "L", "R"]


def find_prev_neighbours(location, grid_shape):
    # location is a 4-vector: x, y, entry_dir, count
    x, y, entry_dir, count = location
    if entry_dir == 0:  # U
        prev_x, prev_y = x+1, y
    elif entry_dir == 1:  # D
        prev_x, prev_y = x-1, y
    elif entry_dir == 2:  # L
        prev_x, prev_y = x, y+1
    elif entry_dir == 3:  # R
        prev_x, prev_y = x, y-1
    else:
        raise ValueError(f"Entry direction {entry_dir} not understood")

    if prev_x < 0 or prev_x >= grid_shape[0]:
        return []

    if prev_y < 0 or prev_y >= grid_shape[1]:
        return []

    if count > 0:  # awkwardly zero indexed
        prev_counts = [count - 1]
        prev_dirs = [entry_dir]
    else:
        prev_counts = [0, 1, 2]  # i.e. any, it changed direction
        if entry_dir in [0, 1]:
            prev_dirs = [2, 3]
        elif entry_dir in [2, 3]:
            prev_dirs = [0, 1]
        else:
            raise ValueError(f"Entry direction {entry_dir} not understood")

    neighbours = []
    for prev_dir in prev_dirs:
        for prev_count in prev_counts:
            neighbours.append((prev_x, prev_y, prev_dir, prev_count))

    return neighbours


def find_prev_neighbours_2(location, grid_shape):
    # location is a 4-vector: x, y, entry_dir, count
    x, y, entry_dir, count = location
    if entry_dir == 0:  # U
        prev_x, prev_y = x+1, y
    elif entry_dir == 1:  # D
        prev_x, prev_y = x-1, y
    elif entry_dir == 2:  # L
        prev_x, prev_y = x, y+1
    elif entry_dir == 3:  # R
        prev_x, prev_y = x, y-1
    else:
        raise ValueError(f"Entry direction {entry_dir} not understood")

    if prev_x < 0 or prev_x >= grid_shape[0]:
        return []

    if prev_y < 0 or prev_y >= grid_shape[1]:
        return []

    if count > 0:  # i.e. didn't turn previously
        prev_counts = [count - 1]
        prev_dirs = [entry_dir]
    else:
        prev_counts = [3, 4, 5, 6, 7, 8, 9]  # i.e. any, it changed direction
        if entry_dir in [0, 1]:
            prev_dirs = [2, 3]
        elif entry_dir in [2, 3]:
            prev_dirs = [0, 1]
        else:
            raise ValueError(f"Entry direction {entry_dir} not understood")

    neighbours = []
    for prev_dir in prev_dirs:
        for prev_count in prev_counts:
            neighbours.append((prev_x, prev_y, prev_dir, prev_count))

    return neighbours


def dijkstra_ish(grid, neighbour_fun=find_prev_neighbours, n_steps=(0, 3)):
    dummy_val = np.sum(grid)
    distance_grid = dummy_val * np.ones(grid.shape + (4, n_steps[1]), dtype=int)
    distance_grid[-1, -1] = 0

    end_point = grid.shape[0] - 1, grid.shape[1] - 1

    # frontier = [end_point + (i, j) for i in range(4) for j in range(*n_steps)]
    frontier = np.zeros(distance_grid.shape, dtype=bool)
    frontier[-1, -1, :, tuple(range(*n_steps))] = True
    n_frontier = np.sum(frontier)

    # resolved_points = []
    resolved_points = np.zeros(distance_grid.shape, dtype=bool)
    n_resolved = 0

    total_points_to_resolve = grid.shape[0] * grid.shape[1] * n_steps[1] * 4
    while n_frontier > 0:
        if (total_points_to_resolve - n_resolved) % 100 == 0:
            print(f"\r{total_points_to_resolve - n_resolved}", end="")

        # array_front = np.where(frontier)
        # distance_at_trials = distance_grid[
        #     array_front[:, 0],
        #     array_front[:, 1],
        #     array_front[:, 2],
        #     array_front[:, 3],
        # ]
        # distance_at_trials = distance_grid[array_front]

        # test_point = frontier[np.argmin(distance_at_trials)]
        test_point = tuple(np.argwhere(frontier)[np.argmin(distance_grid[frontier])])

        # test_point = None
        # best_val = dummy_val
        # for point in frontier:
        #     if distance_grid[point] < best_val:
        #         test_point = point
        #         best_val = distance_grid[point]
        # if test_point is None:
        #     break

        # frontier.remove(test_point)
        frontier[test_point] = False
        n_frontier -= 1

        new_value = distance_grid[test_point] + grid[test_point[:2]]
        neighbours = neighbour_fun(test_point, grid.shape)
        for neighbour in neighbours:
            if resolved_points[neighbour]:
                continue

            distance_grid[neighbour] = min(distance_grid[neighbour], new_value)
            if not frontier[neighbour]:
                n_frontier += 1
                frontier[neighbour] = True
            # if neighbour not in frontier:
                # frontier.append(neighbour)

        n_resolved += 1
        resolved_points[test_point] = True

    print("\rDone")
    return distance_grid


if __name__ == "__main__":
    text = common.import_file("input/day17")
    grid = parse_input(text)

    demo_text = r"""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

    demo_grid = parse_input(demo_text)

    distance_grid = dijkstra_ish(demo_grid)
    common.part(1, np.min(distance_grid[0, 0]))

    distance_grid = dijkstra_ish(demo_grid, neighbour_fun=find_prev_neighbours_2, n_steps=(3, 10))
    common.part(2, np.min(distance_grid[0, 0]))

    demo_text_2 = """111111111111
999999999991
999999999991
999999999991
999999999991"""

    demo_grid_2 = parse_input(demo_text_2)
    distance_grid = dijkstra_ish(demo_grid_2, neighbour_fun=find_prev_neighbours_2, n_steps=(3, 10))
    common.part(2, np.min(distance_grid[0, 0]))

    # distance_grid = dijkstra_ish(grid)
    # common.part(1, np.min(distance_grid[0, 0]))

    distance_grid = dijkstra_ish(grid, neighbour_fun=find_prev_neighbours_2, n_steps=(3, 10))
    common.part(2, np.min(distance_grid[0, 0]))  # This isn't quite right
