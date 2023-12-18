import numpy as np

import common


def parse_input(text):
    parsed_input = []
    for line in text.split("\n"):
        if line == "":
            continue
        direction, length, colour = line.split()
        colour = colour[2:-1]

        parsed_input.append((direction, int(length), colour))

    return parsed_input


def reparse_input(parsed_input):
    new_input = []
    dir_map = {
        "0": "R",
        "1": "D",
        "2": "L",
        "3": "U"
    }
    for _, _, colour in parsed_input:
        direction = dir_map[colour[-1]]
        length = int(colour[:-1], 16)
        new_input.append((direction, length, None))

    return new_input



def draw_edge(input):
    current_point = (0, 0)
    all_points = []
    all_segments = []

    all_points.append(current_point)

    for direction, length, colour in input:
        if direction == "R":
            current_point = current_point[0], current_point[1] + length
        elif direction == "L":
            current_point = current_point[0], current_point[1] - length
        elif direction == "U":
            current_point = current_point[0] - length, current_point[1]
        elif direction == "D":
            current_point = current_point[0] + length, current_point[1]
        else:
            raise ValueError(f"Direction {direction} not understood")

        all_points.append(current_point)
        all_segments.append(colour)

    return all_points, all_segments


def draw_edge_on_array(input):
    all_points, all_segments = draw_edge(input)
    min_x = min(point[0] for point in all_points)
    min_y = min(point[1] for point in all_points)
    max_x = max(point[0] for point in all_points)
    max_y = max(point[1] for point in all_points)

    shifted_points = [
        (point[0] - min_x, point[1] - min_y)
        for point in all_points
    ]

    array = np.zeros(((max_x-min_x)+1, (max_y-min_y)+1))

    for point_from, point_to in zip(shifted_points[:-1], shifted_points[1:]):
        if point_from[0] == point_to[0]:
            array[point_from[0], min(point_from[1], point_to[1]):max(point_from[1], point_to[1])+1] = 1
        elif point_from[1] == point_to[1]:
            array[min(point_from[0], point_to[0]):max(point_from[0], point_to[0])+1, point_from[1]] = 1
        else:
            raise ValueError("Line doesn't appear to be flat")

    padded_array = np.zeros((array.shape[0] + 2, array.shape[1] + 2))
    padded_array[1:-1, 1:-1] = array
    return padded_array


def fill_outside(array):
    outside_map = np.zeros_like(array, dtype=bool)
    outside_map[0, :] = True
    outside_map[-1, :] = True
    outside_map[:, 0] = True
    outside_map[:, -1] = True

    n_outside = np.sum(outside_map)
    while True:
        for i_row in range(1, array.shape[0]-1):
            for i_col in range(1, array.shape[1]-1):
                if outside_map[i_row, i_col]:
                    continue
                elif array[i_row, i_col] != 0:
                    continue

                if outside_map[i_row-1, i_col]:
                    outside_map[i_row, i_col] = 1
                elif outside_map[i_row+1, i_col]:
                    outside_map[i_row, i_col] = 1
                elif outside_map[i_row, i_col+1]:
                    outside_map[i_row, i_col] = 1
                elif outside_map[i_row, i_col-1]:
                    outside_map[i_row, i_col] = 1

        if n_outside == np.sum(outside_map):
            break
        else:
            n_outside = np.sum(outside_map)

    return outside_map


if __name__ == "__main__":
    text = common.import_file("input/day18")

    demo_text = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

    parsed_input = parse_input(text)
    array = draw_edge_on_array(parsed_input)
    outside_map = fill_outside(array)
    common.part(1, outside_map.shape[0] * outside_map.shape[1] - np.sum(outside_map))

    new_input = reparse_input(parsed_input)
    array = draw_edge_on_array(new_input)
    outside_map = fill_outside(array)
    common.part(2, outside_map.shape[0] * outside_map.shape[1] - np.sum(outside_map))