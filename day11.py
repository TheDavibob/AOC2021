import numpy as np
import common


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.flash_count = 0

    def step(self):
        self.grid += 1

        while np.any(self.grid >= 10):
            flash_grid = self.grid >= 10

            for row in range(self.grid.shape[0]):
                for col in range(self.grid.shape[1]):
                    if (self.grid[row, col] > 0) and (self.grid[row, col] < 10):
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                if (row + dx >= 0) and (row + dx < self.grid.shape[0]) and (col + dy >= 0) and (col + dy < self.grid.shape[1]):
                                    if (flash_grid[row+dx, col+dy]) and ((dx, dy) != (0, 0)):
                                        self.grid[row, col] += 1

            self.grid[flash_grid] = 0

        self.flash_count += np.sum(self.grid == 0)



if __name__ == "__main__":
    text = common.import_file("input/day11_input")
    grid = common.convert_string_to_np_array(text, {str(t): t for t in range(10)})

    g = Grid(grid)
    for _ in range(100):
        g.step()

    print(f"Part 1: {g.flash_count}")

    grid = common.convert_string_to_np_array(text, {str(t): t for t in range(10)})
    g = Grid(grid)
    counter = 0
    while True:
        g.step()
        counter += 1
        if np.all(g.grid == 0):
            print(f"Part 2: {counter}")
            break