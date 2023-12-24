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

def math(stones):
    positions = np.array([s[0] for s in stones])
    min_pos = int(np.round(np.min(positions)))
    positions -= min_pos
    velocities = np.array([s[1] for s in stones])

    D_matrix = np.zeros((3, len(positions), len(positions)))
    E_matrix = np.zeros((3, len(velocities), len(velocities)))

    for i_t in range(len(positions)):
        for i_o in range(len(positions)):
            D_matrix[:, i_t, i_o] = positions[i_t] - positions[i_o]
            E_matrix[:, i_t, i_o] = velocities[i_t] - velocities[i_o]

    core_matrix = np.zeros((4, 4))
    core_matrix[:, 0] = D_matrix[0, 1:5, 0]
    core_matrix[:, 1] = E_matrix[2, 1:5, 0]
    core_matrix[:, 2] = -D_matrix[2, 1:5, 0]
    core_matrix[:, 3] = -E_matrix[0, 1:5, 0]

    forcing_bit = D_matrix[0, 1:5, 0] * E_matrix[2, 1:5, 0] - E_matrix[0, 1:5, 0] * D_matrix[2, 1:5, 0]

    soln = np.linalg.solve(core_matrix, forcing_bit)

    W = soln[0]
    X = soln[1]
    U = soln[2]
    Z = soln[3]

    Xb = X + positions[0, 0]
    Zb = Z + positions[0, 2]
    Ub = U + velocities[0, 0]
    Wb = W + velocities[0, 2]

    t0 = - X / U

    # Bit bemused by the below
    t1 = - (X + D_matrix[0, 0, 1])/(U + E_matrix[0, 0, 1])

    Vb = ((positions[1, 1] - positions[0, 1]) + (t1 * velocities[1, 1] - t0 * velocities[0, 1])) / (t1 - t0)
    Yb = positions[0, 1] + t0 * (velocities[0, 1] - Vb)

    # Note, the pos is scaled down by the min
    start_pos = (int(np.round(Xb)), int(np.round(Yb)), int(np.round(Zb)))
    start_vel = (int(np.round(Ub)), int(np.round(Vb)), int(np.round(Wb)))

    return sum(start_pos) + 3*min_pos

    # total = 0
    # for stone in stones:
    #     position, velocity = stone
    #     relative_position = [p - min_pos - q for (p, q) in zip(position, start_pos)]
    #     relative_velocity = [p - q for (p, q) in zip(velocity, start_vel)]
    #
    #     time = - relative_position[0] / relative_velocity[0]
    #
    #     true_position = [int(round(p + time * v)) for p, v in zip(position, velocity)]
    #
    #     total += sum(true_position)

    return total



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

    assert math(demo_stones) == 47

    common.part(2, math(stones))

