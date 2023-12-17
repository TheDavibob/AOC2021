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


class ShortestPathFinder:
    def __init__(self, grid):
        self.grid = grid

        self.lower_corner = (grid.shape[0]-1, grid.shape[1]-1)

        self.memo_dict = {}

    def shortest_path(self, location, prev_direction, prev_in_direction, visited_before):
        memoised_path = self.memo_dict.get((location, prev_direction, prev_in_direction), None)
        if memoised_path is not None:
            return memoised_path

        if ((location, prev_direction, prev_in_direction)) in visited_before:
            return float('inf')

        # This is *branch* specific, to prevent loops
        visited_before = visited_before + [(location, prev_direction, prev_in_direction)]

        if location == self.lower_corner:
            print(visited_before)
            self.memo_dict[(location, prev_direction, prev_in_direction)] = self.grid[location]
            return self.grid[location]

        if prev_direction in ["L", "R"]:
            new_directions = ["U", "D"]
        elif prev_direction in ["U", "D"]:
            new_directions = ["L", "R"]
        # elif prev_direction == "N":
        #     new_directions = ["L", "R", "U", "D"]
        else:
            raise ValueError(f"Direction {prev_direction} not understood.")

        if prev_in_direction < 3:
            new_directions.append(prev_direction)

        best_new_path = float('inf')
        for direction in new_directions:
            if direction == prev_direction:
                new_prev_in_dir = prev_in_direction + 1
            else:
                new_prev_in_dir = 1

            if direction == "R":
                if location[1] + 1 >= self.grid.shape[1]:
                    continue

                new_location = (location[0], location[1] + 1)
            elif direction == "L":
                if location[1] - 1 < 0:
                    continue
                new_location = (location[0], location[1] - 1)
            elif direction == "U":
                if location[0] - 1 < 0:
                    continue
                new_location = (location[0] - 1, location[1])
            elif direction == "D":
                if location[0] + 1 >= self.grid.shape[0]:
                    continue
                new_location = (location[0] + 1, location[1])
            else:
                raise ValueError(f"Direction {direction} not understood")

            new_path = self.shortest_path(new_location, direction, new_prev_in_dir, visited_before)

            best_new_path = min(new_path, best_new_path)

        total_path = best_new_path + self.grid[location]

        self.memo_dict[(location, prev_direction, prev_in_direction)] = total_path

        return total_path

    def run(self):
        path_one = self.shortest_path((0, 1), "R", 1, [])
        path_two = self.shortest_path((1, 0), "D", 1, [])
        return min(path_one, path_two)


# Grid approach - the one above didn't work
DIRECTIONS = ["U", "D", "L", "R"]


def find_neighbours(location, grid_shape):
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


def dijkstra_ish(grid):
    distance_grid = np.sum(grid) * np.ones(grid.shape + (4, 3), dtype=int)
    distance_grid[-1, -1] = 0

    end_point = grid.shape[0] - 1, grid.shape[1] - 1

    frontier = deque(end_point + (i, j) for i in range(4) for j in range(3))

    resolved_points = []
    while len(frontier) > 0:
        test_point = frontier.popleft()

        new_value = distance_grid[test_point] + grid[test_point[:2]]
        neighbours = find_neighbours(test_point, grid.shape)
        for neighbour in neighbours:
            # if neighbour in resolved_points:
            #     continue

            if (neighbour not in frontier) and (neighbour not in resolved_points):
                frontier.append(neighbour)

            if neighbour == (2, 9, 3, 0):
                print(test_point, new_value)
            distance_grid[neighbour] = min(distance_grid[neighbour], new_value)

        resolved_points.append(test_point)

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