import numpy as np
import common


def parse_input(text):
    lines = text.split("\n")
    height = len([line for line in lines if line != ""])
    width = len(lines[0])
    array = np.zeros((height, width), dtype=np.int32)
    for i_line, line in enumerate(lines):
        if line == "":
            continue

        for i_char, char in enumerate(line):
            if char == "S":
                array[i_line, i_char] = 0
                start = (i_line, i_char)
            elif char == "E":
                array[i_line, i_char] = 25
                end = (i_line, i_char)
            else:
                array[i_line, i_char] = ord(char) - ord("a")

    return array, start, end


def step(height_grid, distance_grid):
    new_distance_grid = distance_grid.copy()

    for i in range(height_grid.shape[0]):
        for j in range(height_grid.shape[1]):
            current_height = height_grid[i, j]
            current_dist = distance_grid[i, j]

            if current_dist != -1:
                continue

            if distance_grid[i, j] != -1:
                continue

            if i > 0:
                up = distance_grid[i-1, j]
                height_up = height_grid[i-1, j]
            else:
                up = -1
                height_up = 0

            if j > 0:
                left = distance_grid[i, j-1]
                height_left = height_grid[i, j-1]
            else:
                left = -1
                height_left = 0

            if i < height_grid.shape[0] - 1:
                down = distance_grid[i+1, j]
                height_down = height_grid[i+1, j]
            else:
                down = -1
                height_down = 0

            if j < height_grid.shape[1] - 1:
                right = distance_grid[i, j+1]
                height_right = height_grid[i, j+1]
            else:
                right = -1
                height_right = 0

            if current_dist > -1:
                possible_dists = [current_dist]
            else:
                possible_dists = []

            if all(a == -1 for a in [up, down, left, right]):
                continue

            for dist, height in zip([up, down, left, right], [height_up, height_down, height_left, height_right]):
                if dist == -1:
                    continue

                if height - current_height >= 2:
                    continue

                else:
                    possible_dists.append(dist+1)

            if len(possible_dists) > 0:
                # new_distance_grid[i, j] = min(possible_dists)
                distance_grid[i, j] = min(possible_dists)

    return distance_grid


if __name__ == "__main__":
    text = common.load_todays_input(__file__)
#     text = """Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi"""
    height_grid, start, end = parse_input(text)
    distance_grid = -np.ones(height_grid.shape, dtype=np.int32)
    distance_grid[end] = 0

    old_distance_grid = distance_grid.copy()
    while True:
        distance_grid = step(height_grid, distance_grid)
        if np.all(distance_grid == old_distance_grid):
            break

        old_distance_grid = distance_grid.copy()

    common.part(1, distance_grid[start])

    min_dist = distance_grid[start]
    for i in range(height_grid.shape[0]):
        for j in range(height_grid.shape[1]):
            if height_grid[i, j] != 0:
                continue
            if distance_grid[i, j] == -1:
                continue

            min_dist = min(distance_grid[i, j], min_dist)

    common.part(2, min_dist)
