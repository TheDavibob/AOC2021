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

        # if visited_map[current_position]:
        #     break

        visited_map[current_position] = True

    return n_steps, np.sum(visited_map)


def check_for_loop(array):
    obstacle_map = (array == 1)
    current_position = np.where(array == 2)
    current_position = (current_position[0][0], current_position[1][0])
    current_direction = np.array([-1, 0])

    visited_map = array == 2
    directions_map = np.zeros(obstacle_map.shape + (4,), dtype=bool)
    current_dir_as_number = direction_to_number(current_direction)
    directions_map[current_position + (current_dir_as_number,)] = True

    loop = False
    while True:
        n_steps, current_position, current_direction = step(
            obstacle_map,
            current_position,
            current_direction
        )
        if n_steps == -1:
            break

        current_dir_as_number = direction_to_number(current_direction)

        if visited_map[current_position] and directions_map[current_position + (current_dir_as_number,)]:
            loop = True
            break

        visited_map[current_position] = True
        directions_map[current_position + (current_dir_as_number,)] = True

    return loop


def direction_to_number(direction):
    if not direction[0]:
        return (direction[1] > 0).astype(int)
    return 2 + (direction[0] > 0).astype(int)


def part_two(array):
    loops = 0
    for i_row in range(array.shape[0]):
        print(f"Row: {i_row}")
        for i_col in range(array.shape[1]):
            new_array = array.copy()
            if new_array[i_row, i_col]:
                continue

            new_array[i_row, i_col] = 1
            new_loop = check_for_loop(new_array)
            if new_loop:
                print((i_row, i_col))

            loops += new_loop

    print(f"Part 2: {loops}")


if __name__ == "__main__":
    with open("input/day6") as file:
        text = file.read()

#     text = """....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#...
# """

    as_array = parse_input(text)
    _, n_visited = part_one(as_array)
    print(f"Part 1: {n_visited}")

    part_two(as_array)
