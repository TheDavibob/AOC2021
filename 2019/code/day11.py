import numpy as np
from matplotlib import pyplot as plt

import common
import intcode

LEFT_MAP = {
    "^": "<",
    "<": "v",
    "v": ">",
    ">": "^"
}

RIGHT_MAP = {v: k for k, v in LEFT_MAP.items()}


class Painting:
    def __init__(self, code, initial_input):
        self.intcode_computer = intcode.Intcode(code, pause_on_no_inputs=True)
        self.intcode_computer.input_list.append(initial_input)
        self.current_position = (0, 0)
        self.current_direction = "^"

        self.painted_white = []
        self.painted_black = []

    def step(self):
        out_code = self.intcode_computer.step_all()
        rotation = self.intcode_computer.output_list.pop()
        colour = self.intcode_computer.output_list.pop()

        if colour:
            if self.current_position not in self.painted_white:
                self.painted_white.append(self.current_position)
                if self.current_position in self.painted_black:
                    self.painted_black.remove(self.current_position)
        else:
            if self.current_position in self.painted_white:
                self.painted_white.remove(self.current_position)
                if self.current_position not in self.painted_black:
                    self.painted_black.append(self.current_position)


        if rotation:
            self.current_direction = RIGHT_MAP[self.current_direction]
        else:
            self.current_direction = LEFT_MAP[self.current_direction]

        if self.current_direction == "^":
            self.current_position = (self.current_position[0], self.current_position[1] + 1)
        elif self.current_direction == "v":
            self.current_position = (self.current_position[0], self.current_position[1] - 1)
        elif self.current_direction == "<":
            self.current_position = (self.current_position[0] - 1, self.current_position[1])
        elif self.current_direction == ">":
            self.current_position = (self.current_position[0] + 1, self.current_position[1])
        else:
            ValueError("Direction not understood")

        if self.current_position in self.painted_white:
            self.intcode_computer.input_list.append(1)
        else:
            self.intcode_computer.input_list.append(0)

        if out_code:
            finished = False
        else:
            finished = True

        return finished

    def step_all(self):
        finished = False
        while not finished:
            finished = self.step()


def draw_grid(points):
    points = np.array(points)
    minima = np.min(points, axis=0)
    maxima = np.max(points, axis=0)

    grid = np.zeros(maxima + 1 - minima, dtype=bool)

    for point in points:
        grid_loc = point - minima
        grid[grid_loc[0], grid_loc[1]] = True

    return grid


if __name__ == "__main__":
    code = common.import_file("../input/day11")
    p = Painting(code, 0)
    p.step_all()
    common.part(1, len(p.painted_white) + len(p.painted_black))

    p = Painting(code, 1)
    p.step_all()
    plt.matshow(draw_grid(p.painted_white).T)
