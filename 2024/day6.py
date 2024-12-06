import numpy as np

import common


def parse_input(text):
    as_array = common.convert_string_to_np_array(
        text,
        {".": 0, "#": 1, "^": 2}
    )

    return as_array


def step(obstacle_array, current_position, current_direction):
    attempt = (
        current_position[0] + current_direction[0],
        current_position[1] + current_direction[1]
    )

    if attempt[0] < 0 or attempt[0] >= obstacle_array.shape[0]:
        return -1, attempt, current_direction
    if attempt[1] < 0 or attempt[1] >= obstacle_array.shape[1]:
        return -1, attempt, current_direction

    if not obstacle_array[attempt]:
        new_position = attempt
        new_direction = current_direction
        return 1, new_position, new_direction

    new_direction = np.array([[0, 1], [-1, 0]]) @ current_direction
    return 0, current_position, new_direction


def part_one(array):
    obstacle_map = (array == 1)
    current_position = np.where(array == 2)
    current_position = (current_position[0][0], current_position[1][0])
    current_direction = np.array([-1, 0])

    visited_map = array == 2
    while True:
        n_steps, current_position, current_direction = step(
            obstacle_map,
            current_position,
            current_direction
        )
        if n_steps == -1:
            break

        visited_map[current_position] = True

    print(f"Part 1: {np.sum(visited_map)}")


if __name__ == "__main__":
    with open("input/day6") as file:
        text = file.read()

    as_array = parse_input(text)
    part_one(as_array)