import numpy as np
import matplotlib.pyplot as plt
import common

def create_grid(text):
    numbers_str, instructions = text.split('\n\n')
    numbers = []
    for line in numbers_str.split('\n'):
        numbers.append([int(s) for s in line.split(',')])

    instructions = [s for s in instructions.split('\n')]
    return numbers, instructions


def numbers_to_grid(numbers):
    extrema = np.max(numbers, axis=0)
    grid = np.zeros(extrema[::-1]+1, dtype=int)
    for n in numbers:
        grid[n[1], n[0]] = 1

    return grid


def fold_x(grid):
    new_grid = grid[:, :(grid.shape[1] // 2)].copy()
    new_grid += grid[:, grid.shape[1] - 1:(grid.shape[1] // 2):-1]
    new_grid[new_grid > 1] = 1
    return new_grid


def fold_y(grid):
    new_grid = grid[:(grid.shape[0] // 2), :].copy()
    new_grid += grid[grid.shape[0] - 1:(grid.shape[0] // 2):-1, :]
    new_grid[new_grid > 1] = 1
    return new_grid



if __name__ == "__main__":
    text = common.import_file("input/day13_input")
    numbers, instructions = create_grid(text)
    grid = numbers_to_grid(numbers)
    print(f"Part 1: {np.sum(fold_x(grid))}")

    for instruction in instructions:
        if instruction != "":
            coord = instruction.split("=")[0][-1]
            if coord == "x":
                grid = fold_x(grid)
            elif coord == "y":
                grid = fold_y(grid)

    plt.matshow(grid)
