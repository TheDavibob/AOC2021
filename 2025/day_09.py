# /// script
# dependencies = [
#   "numpy>=2.0.0",
#   "matplotlib",
# ]
# ///
import numpy as np
import matplotlib.pyplot as plt

TEST_INPUT = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


with open("data/day_09") as f:
    REAL_DATA = f.read()


def part_one(puzzle_input):
    points = []
    for line in puzzle_input.split("\n"):
        point = line.split(",")
        x, y = [int(p) for p in point]
        points.append((x, y))

    points_array = np.array(points)
    deltas = np.abs(points_array[:, None, :] - points_array[None, :, :]) + 1

    areas = np.prod(deltas, axis=-1)

    return np.max(areas)


def part_two(puzzle_input):
    points = []
    for line in puzzle_input.split("\n"):
        point = line.split(",")
        x, y = [int(p) for p in point]
        points.append((x, y))

    points_array = np.array(points)

    # points_shifted = points_array - np.min(points_array, axis=0)

    all_xs = np.unique(points_array[:, 0])
    all_ys = np.unique(points_array[:, 1])

    all_xs = list(all_xs)
    all_ys = list(all_ys)

    points_shifted = []
    for point in points_array:
        new_point = (all_xs.index(point[0]), all_ys.index(point[1]))
        points_shifted.append(new_point)

    points_shifted = np.array(points_shifted)

    grid = np.zeros(np.max(points_shifted, axis=0)+1, dtype=bool)
    for point in points_shifted:
        grid[*point] = True

    for s_point, e_point in zip(points_shifted[:-1], points_shifted[1:]):
        delta = e_point - s_point
        delta = np.round(delta / np.sum(np.abs(delta))).astype(int)

        point = s_point
        while not np.all(point == e_point):
            grid[*point] = True
            point = point + delta

    s_point, e_point = points_shifted[-1], points_shifted[0]
    delta = e_point - s_point
    delta = np.round(delta / np.sum(np.abs(delta))).astype(int)

    point = s_point
    while not np.all(point == e_point):
        grid[*point] = True
        point += delta

    # plt.imshow(grid)
    # plt.show()

    print("Expanding grid")
    new_grid = np.zeros((grid.shape[0]+2, grid.shape[1]+2), dtype=bool)
    new_grid[1:-1, 1:-1] = grid

    print(new_grid.shape)

    is_outside = np.zeros_like(new_grid)
    is_outside[0, :] = True
    is_outside[-1, :] = True
    is_outside[:, 0] = True
    is_outside[:, -1] = True

    is_changed = True
    while is_changed:
        is_changed=False
        for i_row in range(new_grid.shape[0]):
            for i_col in range(new_grid.shape[1]):
                if is_outside[i_row, i_col]:
                    continue
                if new_grid[i_row, i_col]:
                    continue

                if i_col > 0 and is_outside[i_row, i_col-1]:
                    is_outside[i_row, i_col] = True
                    is_changed = True
                elif i_col < new_grid.shape[1] and is_outside[i_row, i_col+1]:
                    is_outside[i_row, i_col] = True
                    is_changed = True
                elif i_row > 0 and is_outside[i_row-1, i_col]:
                    is_outside[i_row, i_col] = True
                    is_changed = True
                elif i_row < new_grid.shape[0] and is_outside[i_row+1, i_col]:
                    is_outside[i_row, i_col] = True
                    is_changed = True
        print(f"Found outside points: {is_outside.sum()}")

    new_grid |= ~is_outside

    grid = new_grid[1:-1, 1:-1]

    print("Finding best area")
    best_area = 0
    for a_point, a_rep in zip(points_array, points_shifted):
        for b_point, b_rep in zip(points_array, points_shifted):
            min_x, max_x = sorted((a_rep[0], b_rep[0]))
            min_y, max_y = sorted((a_rep[1], b_rep[1]))

            min_true_x, max_true_x = sorted((a_point[0], b_point[0]))
            min_true_y, max_true_y = sorted((a_point[1], b_point[1]))

            area = (max_true_x+1-min_true_x) * (max_true_y+1-min_true_y)
            if area <= best_area:
                continue

            this_grid = np.zeros_like(grid)
            this_grid[min_x:max_x+1, min_y:max_y+1] = True

            if np.all(grid[this_grid]):
                best_area = area
                print(f"New best area!: {best_area}")

    return best_area


if __name__ == "__main__":
    assert part_one(TEST_INPUT) == 50
    print(f"Part 1: {part_one(REAL_DATA)}")

    assert part_two(TEST_INPUT) == 24
    print(f"Part 2: {part_two(REAL_DATA)}")