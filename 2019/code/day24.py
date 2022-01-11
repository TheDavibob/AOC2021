import numpy as np
from scipy.signal import convolve2d

import common


class Bugs:
    def __init__(self, grid_str):
        self.grid = common.convert_string_to_np_array(grid_str, {'.': 0, '#': 1})
        self.historical_biodiversity = []

    def step(self):
        self.historical_biodiversity.append(self.biodiversity())

        convolution_grid = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
        neighbour_count = convolve2d(self.grid, convolution_grid, "same")
        new_grid = self.grid.copy()
        new_grid[(self.grid == 1) & (neighbour_count != 1)] = 0
        new_grid[(self.grid == 0) & ((neighbour_count == 2) | (neighbour_count == 1))] = 1

        self.grid = new_grid

    def step_until_repeat(self):
        while self.biodiversity() not in self.historical_biodiversity:
            self.step()

        return self.biodiversity()

    def biodiversity(self):
        return int("".join(str(b) for b in self.grid.flatten())[::-1], 2)


class StackOBugs:
    def __init__(self, grid_str):
        self.grids = [common.convert_string_to_np_array(grid_str, {'.': 0, '#': 1})]
        self.central_grid = 0

    def step(self):
        new_grids = [np.zeros((5, 5), dtype=int)] + [g.copy() for g in self.grids] + [np.zeros((5, 5), dtype=int)]

        for i in range(len(new_grids)):
            grid = new_grids[i]
            if i in [0, 1]:
                inner_grid = np.zeros((5, 5), dtype=int)
            else:
                inner_grid = self.grids[i-2]

            if i in [len(new_grids) - 2, len(new_grids) - 1]:
                outer_grid = np.zeros((5, 5), dtype=int)
            else:
                outer_grid = self.grids[i]

            if i in [0, len(new_grids) - 1]:
                old_grid = np.zeros((5, 5))
            else:
                old_grid = self.grids[i-1]

            bulked_old_grid = np.zeros((7, 7))
            bulked_old_grid[1:-1, 1:-1] = old_grid
            bulked_old_grid[0, 1:-1] = outer_grid[1, 2]
            bulked_old_grid[-1, 1:-1] = outer_grid[3, 2]
            bulked_old_grid[1:-1, 0] = outer_grid[2, 1]
            bulked_old_grid[1:-1, -1] = outer_grid[2, 3]

            convolution_grid = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
            neighbour_count = convolve2d(bulked_old_grid, convolution_grid, "same")[1:-1, 1:-1]

            # While this includes the outer grid, it does not include the inner grid.
            neighbour_count[1, 2] += np.sum(inner_grid[0, :])
            neighbour_count[3, 2] += np.sum(inner_grid[-1, :])
            neighbour_count[2, 1] += np.sum(inner_grid[:, 0])
            neighbour_count[2, 3] += np.sum(inner_grid[:, -1])

            grid[(old_grid == 1) & (neighbour_count != 1)] = 0
            grid[(old_grid == 0) & ((neighbour_count == 2) | (neighbour_count == 1))] = 1
            grid[2, 2] = 0

        self.grids = new_grids
        self.central_grid += 1

        self.trim()

    def trim(self):
        if np.all(self.grids[0] == 0):
            self.grids = self.grids[1:]
            self.central_grid -= 1

        if np.all(self.grids[-1] == 0):
            self.grids = self.grids[:-1]


if __name__ == "__main__":
    grid="""..###
.####
...#.
.#..#
#.###
"""
    bugs = Bugs(grid)
    common.part(1, bugs.step_until_repeat())

    bugs = StackOBugs(grid)
    for _ in range(200):
        bugs.step()
    common.part(2, np.sum(np.array(bugs.grids)))