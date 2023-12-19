import numpy as np
from tqdm import tqdm

import common


def parse_input(text):
    return common.convert_string_to_np_array(
        text,
        {".": 0, "\\": 1, "/": 2, "|": 3, "-": 4}
    )


def step(head, direction, grid):
    if direction == "R":
        if head[1] == grid.shape[1]-1:
            return []

        new_head = head[0], head[1]+1
    elif direction == "L":
        if head[1] == 0:
            return []

        new_head = head[0], head[1] - 1
    elif direction == "U":
        if head[0] == 0:
            return []

        new_head = head[0] - 1, head[1]
    elif direction == "D":
        if head[0] == grid.shape[0]-1:
            return []

        new_head = head[0] + 1, head[1]
    else:
        raise ValueError(f"Direction {direction} not understood")

    object = grid[new_head]

    if object == 0:
        return [(new_head, direction)]
    elif object == 1:
        if direction == "R":
            return [(new_head, "D")]
        elif direction == "D":
            return [(new_head, "R")]
        elif direction == "U":
            return [(new_head, "L")]
        elif direction == "L":
            return [(new_head, "U")]
    elif object == 2:
        if direction == "R":
            return [(new_head, "U")]
        elif direction == "U":
            return [(new_head, "R")]
        elif direction == "D":
            return [(new_head, "L")]
        elif direction == "L":
            return [(new_head, "D")]
    elif object == 3:
        if direction in ["U", "D"]:
            return [(new_head, direction)]
        elif direction in ["L", "R"]:
            return [(new_head, "U"), (new_head, "D")]
    elif object == 4:
        if direction in ["L", "R"]:
            return [(new_head, direction)]
        elif direction in ["U", "D"]:
            return [(new_head, "L"), (new_head, "R")]


def part_one(grid, start_loc=(0, -1)):
    visited_grid = np.zeros_like(grid)

    if start_loc[0] < 0:
        initial_direction = "D"
    elif start_loc[0] >= grid.shape[0]:
        initial_direction = "U"
    elif start_loc[1] < 0:
        initial_direction = "R"
    elif start_loc[1] >= grid.shape[1]:
        initial_direction = "L"
    else:
        raise ValueError(f"Odd start loc: {start_loc}")

    unresolved_heads = [(start_loc, initial_direction)]
    resolved_heads = []

    while unresolved_heads:
        head_to_probe = unresolved_heads.pop()

        loc_to_probe = head_to_probe[0]
        if (0 <= loc_to_probe[0] < grid.shape[0]) and (0 <= loc_to_probe[1] < grid.shape[1]):
            visited_grid[loc_to_probe] += 1

        new_heads = step(*head_to_probe, grid)

        for head in new_heads:
            if head not in resolved_heads:
                unresolved_heads.append(head)

        resolved_heads.append(head_to_probe)

    return np.sum(visited_grid > 0)


def part_two(grid):
    max_value = 0
    for start_row in tqdm(range(grid.shape[0])):
        value = part_one(grid, (start_row, -1))
        if value > max_value:
            max_value = value

        value = part_one(grid, (start_row, grid.shape[0]))
        if value > max_value:
            max_value = value

    for start_col in tqdm(range(grid.shape[1])):
        value = part_one(grid, (-1, start_col))
        if value > max_value:
            max_value = value

        value = part_one(grid, (grid.shape[1], start_col))
        if value > max_value:
            max_value = value

    return max_value


if __name__ == "__main__":
    text = common.import_file("input/day16")
    grid = parse_input(text)

    demo_text = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

    demo_grid = parse_input(demo_text)

    assert part_one(demo_grid, (0, -1)) == 46

    common.part(1, part_one(grid, (0, -1)))

    assert part_two(demo_grid) == 51

    common.part(2, part_two(grid))