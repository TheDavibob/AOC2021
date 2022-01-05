import common
import numpy as np

def iterate(grid):
    after_right = np.zeros_like(grid, dtype=int)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 1:
                if j+1 == grid.shape[1]:
                    if grid[i, 0] == 0:
                        after_right[i, 0] = 1
                    else:
                        after_right[i, j] = 1
                else:
                    if grid[i, j+1] == 0:
                        after_right[i, j+1] = 1
                    else:
                        after_right[i, j] = 1
            elif grid[i, j] == 2:
                after_right[i, j] = 2

    grid = after_right
    after_down = np.zeros_like(grid, dtype=int)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 2:
                if i+1 == grid.shape[0]:
                    if grid[0, j] == 0:
                        after_down[0, j] = 2
                    else:
                        after_down[i, j] = 2
                else:
                    if grid[i+1, j] == 0:
                        after_down[i+1, j] = 2
                    else:
                        after_down[i, j] = 2
            elif grid[i, j] == 1:
                after_down[i, j] = 1

    return after_down


def all_iterate(grid):
    counter = 0
    while True:
        new_grid = iterate(grid)
        counter += 1
        if np.all(new_grid == grid):
            break
        grid = new_grid

    return counter

if __name__ == "__main__":
    text = common.import_file('input/day25_input')
    grid = common.convert_string_to_np_array(text, {'.': 0, '>': 1, 'v': 2})
    print(all_iterate(grid))
