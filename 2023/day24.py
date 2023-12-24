import sys

import numpy as np
from tqdm import tqdm

import common


def parse_input(text):
    each_stone = []
    for line in text.split("\n"):
        if line == "":
            continue
        position, velocity = line.split(" @ ")
        position = [int(p) for p in position.split(", ")]
        velocity = [int(v) for v in velocity.split(", ")]
        each_stone.append((position, velocity))

    return each_stone


def get_horizontal_intersection(stone_0, stone_1):
    dx = -stone_0[0][0] + stone_1[0][0]
    dy = -stone_0[0][1] + stone_1[0][1]

    u_0 = stone_0[1][0]
    u_1 = stone_1[1][0]
    v_0 = stone_0[1][1]
    v_1 = stone_1[1][1]

    if u_1 * v_0 - v_1 * u_0 == 0:
        return None

    t_1 = (u_0 * dy - v_0 * dx) / (u_1 * v_0 - v_1 * u_0)
    t_0 = (dy + v_1 * t_1) / v_0

    if t_1 < 0:
        return None

    if t_0 < 0:
        return None

    x = stone_1[0][0] + t_1 * u_1
    y = stone_1[0][1] + t_1 * v_1

    return x, y


def part_one(stones, test_area):
    count = 0
    for i_stone, stone in enumerate(stones[:-1]):
        for i_stone_2, stone_2 in enumerate(stones[i_stone+1:]):
            intersection_point = get_horizontal_intersection(stone, stone_2)
            if intersection_point is None:
                continue
            if (
                test_area[0] <= intersection_point[0] <= test_area[1]
                and test_area[0] <= intersection_point[1] <= test_area[1]
            ):
                count += 1

    return count


if __name__ == "__main__":
    text = common.import_file("input/day24")
    stones = parse_input(text)

    demo_text = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
    demo_stones = parse_input(demo_text)

    assert part_one(demo_stones, (7, 27)) == 2

    common.part(1, part_one(stones, (200000000000000, 400000000000000)))