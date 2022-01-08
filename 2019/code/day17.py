import numpy as np
from scipy.signal import convolve2d

import common, intcode

LEFT_MAP = {
    "W": "S",
    "S": "E",
    "E": "N",
    "N": "W"
}
RIGHT_MAP = {v: k for k, v in LEFT_MAP.items()}


def find_intersections(map_grid):
    convolve_grid = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    neighbour_count = convolve2d((map_grid >= 0), convolve_grid, 'same')
    intersections = np.where(neighbour_count == 5)
    cumulative_sum = 0
    intersection_list = []
    for i, j in zip(*intersections):
        cumulative_sum += i * j
        intersection_list.append((i, j))
    return intersection_list, cumulative_sum


def find_lines(point, map_grid):
    point = np.array(point)
    if map_grid[point[0], point[1]] == -1:
        return

    points = []
    directions = (
        [0, 1],
        [0, -1],
        [1, 0],
        [-1, 0]
    )
    for d in directions:
        search_point = point + d
        while True:
            if np.any(search_point) < 0:
                break

            if np.any(search_point >= np.array(map_grid.shape)):
                break

            valid = map_grid[search_point[0], search_point[1]] >= 0
            if not valid:
                break

            search_point = search_point + d

        end_point = search_point - d
        points.append(end_point)

    unique_points = np.unique(points, axis=0)

    if len(unique_points) in [2, 3]:
        if unique_points[0][0] == unique_points[1][0]:
            horz_pair = None
            row = unique_points[0][0]
            vert_pair = ((row, min(unique_points[:, 1])), (row, max(unique_points[:, 1])))
        else:
            vert_pair = None
            col = unique_points[0][1]
            horz_pair = ((min(unique_points[:, 0]), col), (max(unique_points[:, 0]), col))
    else:
        row = point[0]
        cols = unique_points[unique_points[:, 0] == row][:, 1]
        vert_pair = ((row, min(cols)), (row, max(cols)))

        col = point[1]
        rows = unique_points[unique_points[:, 1] == col][:, 0]
        horz_pair = ((min(rows), col), (max(rows), col))

    lines = []
    if horz_pair:
        lines.append(horz_pair)
    if vert_pair:
        lines.append(vert_pair)

    return lines


def get_all_lines(map_grid):
    lines = []
    for i in range(map_grid.shape[0]):
        for j in range(map_grid.shape[1]):
            new_lines = find_lines((i, j), map_grid)
            if new_lines:
                for line in new_lines:
                    if line and (line not in lines):
                        lines.append(line)

    return lines


def trace_route(lines, start_point):
    route_nodes = [start_point]
    route_edges = []

    line_from_start = [l for l in lines if route_nodes[-1] in l][0]
    route_edges.append(line_from_start)
    new_node = [n for n in line_from_start if n != route_nodes[-1]][0]
    route_nodes.append(new_node)

    while True:
        lines_through_point = [l for l in lines if route_nodes[-1] in l]
        if len(lines_through_point) == 1:
            break

        new_line = [l for l in lines_through_point if l not in route_edges][0]
        route_edges.append(new_line)
        new_node = [n for n in new_line if n != route_nodes[-1]][0]
        route_nodes.append(new_node)

    return route_nodes


def get_string_repr(route_nodes):
    len_dir_list = []
    for from_node, to_node in zip(route_nodes[:-1], route_nodes[1:]):
        if to_node[0] == from_node[0]:
            if to_node[1] > from_node[1]:
                direction = 'E'
                length = to_node[1] - from_node[1]
            else:
                direction = 'W'
                length = from_node[1] - to_node[1]
        else:
            if to_node[0] > from_node[0]:
                direction = 'S'
                length = to_node[0] - from_node[0]
            else:
                direction = 'N'
                length = from_node[0] - to_node[0]

        len_dir_list.append((length, direction))

    prev_direction = 'N'
    string_list = []
    for length, direction in len_dir_list:
        if direction == LEFT_MAP[prev_direction]:
            string_list.append('L')
        elif direction == RIGHT_MAP[prev_direction]:
            string_list.append('R')
        else:
            raise ValueError("unexepcted direction")

        prev_direction = direction
        string_list.append(str(length))

    return string_list


def run_part_2(code, main_routine, A, B, C, view=False):
    code = [int(s) for s in code.split(',')]
    code[0] = 2
    s = intcode.Intcode(code)
    for c in ",".join(main_routine):
        s.input_list.append(ord(c))

    s.input_list.append(10)

    for routine in (A, B, C):
        for c in ",".join(routine):
            s.input_list.append(ord(c))
        s.input_list.append(10)

    if view:
        s.input_list.append(ord('y'))
    else:
        s.input_list.append(ord('n'))
    s.input_list.append(10)

    s.step_all()

    return s.output_list


if __name__ == "__main__":
    code = common.import_file('../input/day17')
    computer = intcode.Intcode(code)
    computer.step_all()
    map_code = computer.output_list
    map_string = "".join(chr(i) for i in map_code)
    map_grid = common.convert_string_to_np_array(map_string, {".": -1, "#": 0, "^": 1})
    intersections, cumsum = find_intersections(map_grid)
    common.part(1, cumsum)

    lines = get_all_lines(map_grid)
    route_nodes = trace_route(lines, (int(np.where(map_grid == 1)[0]), int(np.where(map_grid == 1)[1])))
    string_list = get_string_repr(route_nodes)

    # The next bit is a bit manual, but chunks can be found by e.g.:
    full_string = ",".join(string_list)
    full_string.count(",".join(string_list[0:8]))  # This repeats 3 times

    A = string_list[0:8]
    B = string_list[8:14]
    C = string_list[28:36]
    assert A + B + A + B + C + B + A + C + B + C == string_list
    main_routine = "A + B + A + B + C + B + A + C + B + C".split(" + ")

    common.part(2, run_part_2(code, main_routine, A, B, C)[-1])