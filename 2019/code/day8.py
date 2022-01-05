import numpy as np
from matplotlib import pyplot as plt

import common

def make_grid(text, width, height):
    text = text.replace("\n", "")
    n_layers = len(text) // (width * height)
    grid = np.zeros((n_layers, height, width), dtype=int)

    layer, row, col = 0, 0, 0
    for s in text:
        grid[layer, row, col] = int(s)
        col += 1
        if col == width:
            col = 0
            row += 1
            if row == height:
                row = 0
                layer += 1

    return grid


def layer_with_fewest_zeros(grid):
    min_zeros = grid.shape[1] * grid.shape[2]
    num_1s = 0
    num_2s = 0
    for layer in grid:
        count_zeros = np.sum(layer == 0)
        if count_zeros < min_zeros:
            min_zeros = count_zeros
            num_1s = np.sum(layer == 1)
            num_2s = np.sum(layer == 2)

    return min_zeros, num_1s * num_2s


def stack_grid(grid):
    image = grid[0]
    for layer in grid:
        image[image == 2] = layer[image == 2]

    return image


if __name__ == "__main__":
    text = common.import_file("../input/day8")
    grid = make_grid(text, 25, 6)
    print(layer_with_fewest_zeros(grid)[1])

    image = stack_grid(grid)
    plt.matshow(image)