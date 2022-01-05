from copy import copy

import numpy as np

import common


class Grid:
    def __init__(self):
        self.points = [(0, 0)]
        self.line_segments = []
        self.weight_so_far = 0

    def add_point(self, instruction):
        current_location = self.points[-1]
        direction = instruction[0]
        length = int(instruction[1:])
        if direction == "L":
            final_location = (current_location[0] - length, current_location[1])
        elif direction == "R":
            final_location = (current_location[0] + length, current_location[1])
        elif direction == "U":
            final_location = (current_location[0], current_location[1] + length)
        elif direction == "D":
            final_location = (current_location[0], current_location[1] - length)
        else:
            raise ValueError(f"Direction {direction} not understood")

        self.points.append(final_location)

        if direction in ["L", "R"]:
            self.line_segments.append(("H", current_location, final_location, copy(self.weight_so_far)))
        else:
            self.line_segments.append(("V", current_location, final_location, copy(self.weight_so_far)))

        self.weight_so_far += length

    def add_all_points(self, points_str):
        for point in points_str.split(','):
            self.add_point(point)


def do_lines_intersect(line_segment_0, line_segment_1):
    direction_0, start_0, end_0, weight_0 = line_segment_0
    direction_1, start_1, end_1, weight_1 = line_segment_1

    if direction_1 == direction_0:
        return False, None, None

    if direction_0 == "H":
        hor_start, hor_end = start_0, end_0
        ver_start, ver_end = start_1, end_1
    else:
        hor_start, hor_end = start_1, end_1
        ver_start, ver_end = start_0, end_0

    min_0 = min(hor_start[0], hor_end[0])
    max_0 = max(hor_start[0], hor_end[0])
    if (min_0 > ver_start[0]) or (max_0 < ver_start[0]):
        return False, None, None

    min_1 = min(ver_start[1], ver_end[1])
    max_1 = max(ver_start[1], ver_end[1])
    if (min_1 > hor_start[1]) or (max_1 < hor_start[1]):
        return False, None, None

    intersection_point = (ver_start[0], hor_start[1])
    extra_distance = abs(ver_start[0] - hor_start[0]), abs(ver_start[1] - hor_start[1])
    distance = weight_0 + weight_1 + extra_distance[0] + extra_distance[1]

    return True, intersection_point, distance


def get_all_intersections(grid0, grid1):
    intersections = []
    distances = []
    for i_line in grid0.line_segments:
        for j_line in grid1.line_segments:
            do_intersect, location, distance = do_lines_intersect(i_line, j_line)
            if do_intersect:
                intersections.append(location)
                distances.append(distance)

    return intersections, distances


if __name__ == "__main__":
    input = common.import_file("../input/day3")
    grids = [Grid() for _ in range(2)]
    for line, grid in zip(input.split('\n'), grids):
        grid.add_all_points(line)

    intersections, distances = get_all_intersections(*grids)
    print(f"Part 1: {min([abs(i[0]) + abs(i[1]) for i in intersections if i != (0, 0)])}")
    print(f"Part 2: {min(distances)}")
