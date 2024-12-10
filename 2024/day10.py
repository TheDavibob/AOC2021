import numpy as np

import common


directions = [
    (0, 1),
    (1, 0),
    (-1, 0),
    (0, -1),
]

def parse_input(text):
    return common.convert_string_to_np_array(text, {str(x): int(x) for x in range(10)})


def find_paths_from_point(point, map):
    value = map[point]
    if value == 9:
        return [point]

    useful_points = []
    for direction in directions:
        new_point = point[0] + direction[0], point[1] + direction[1]
        if new_point[0] < 0:
            continue
        if new_point[1] < 0:
            continue
        if new_point[0] >= map.shape[0]:
            continue
        if new_point[1] >= map.shape[1]:
            continue

        new_value = map[new_point]
        if new_value == value + 1:
            useful_points.extend(find_paths_from_point(new_point, map))

    return useful_points


def part_one(map):
    possible_points = np.where(map==0)
    score = 0
    for point in zip(possible_points[0], possible_points[1]):
        end_points = find_paths_from_point(point, map)
        score += len(set(end_points))

    print(f"Part 1: {score}")


def part_two(map):
    possible_points = np.where(map==0)
    score = 0
    for point in zip(possible_points[0], possible_points[1]):
        end_points = find_paths_from_point(point, map)
        score += len(end_points)

    print(f"Part 2: {score}")


if __name__ == "__main__":
    with open("input/day10") as file:
        text = file.read()

    map = parse_input(text)
    part_one(map)
    part_two(map)
