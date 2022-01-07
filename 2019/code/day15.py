import random

import numpy as np
from matplotlib import pyplot as plt

import common
import intcode

RIGHT_MAP = {
    1: 4,
    2: 3,
    3: 1,
    4: 2
}

LEFT_MAP = {v: k for k, v in RIGHT_MAP.items()}


class MapMaker:
    def __init__(self, code: str):
        self.intcode = intcode.Intcode(code, pause_on_no_inputs=True)
        self.position = (0, 0)
        self.open_list = [self.position]
        self.open_distance = [0]
        self.wall_list = []
        self.oxygen_list = []
        self.oxy_distance = []

        self.fig, self.ax = plt.subplots()

    def step_on_input(self, direction_input):
        try:
            position_index = self.open_list.index(self.position)
            current_distance = self.open_distance[position_index]
        except ValueError:
            position_index = self.oxygen_list.index(self.position)
            current_distance = self.oxy_distance[position_index]

        if direction_input == 1: # N
            new_position = (self.position[0], self.position[1] + 1)
        elif direction_input == 2: # S
            new_position = (self.position[0], self.position[1] - 1)
        elif direction_input == 3: # W
            new_position = (self.position[0] - 1, self.position[1])
        elif direction_input == 4: # E
            new_position = (self.position[0] + 1, self.position[1])
        else:
            ValueError('Direction input not understood')

        self.intcode.input_list.append(direction_input)
        self.intcode.step_all()
        output = self.intcode.output_list.pop()

        if output in [1, 2]:
            self.position = new_position

        if output == 0:
            if new_position not in self.wall_list:
                self.wall_list.append(new_position)
        elif output == 1:
            if new_position not in self.open_list:
                self.open_list.append(new_position)
                self.open_distance.append(current_distance + 1)
        elif output == 2:
            if new_position not in self.oxygen_list:
                self.oxygen_list.append(new_position)
                self.oxy_distance.append(current_distance + 1)

        return output

    def render(self, type="walls"):
        if type == "none":
            return

        open = np.array(self.open_list)

        if self.wall_list:
            wall = np.array(self.wall_list)
        else:
            wall = np.zeros((0, 2), dtype=int)

        if self.oxygen_list:
            oxygen = np.array(self.oxygen_list)
        else:
            oxygen = np.zeros((0, 2), dtype=int)

        all_points = np.vstack((open, wall, oxygen))
        minima = np.min(all_points, axis=0)
        maxima = np.max(all_points, axis=0)

        grid = np.zeros((maxima - minima + 1), dtype=int)

        if type == "walls":
            grid[open[:, 0]-minima[0], open[:, 1]-minima[1]] = 1
            grid[wall[:, 0]-minima[0], wall[:, 1]-minima[1]] = 2
            grid[oxygen[:, 0]-minima[0], oxygen[:, 1]-minima[1]] = 3

            grid[self.position[0]-minima[0], self.position[1]-minima[1]] = 4
        else:
            grid.fill(-1)
            grid[open[:, 0]-minima[0], open[:, 1]-minima[1]] = self.open_distance
            grid[oxygen[:, 0]-minima[0], oxygen[:, 1]-minima[1]] = self.oxy_distance

        self.ax.clear()
        self.ax.matshow(grid.T)
        plt.pause(0.001)

    def check_neighbours(self, cell):
        neighbours = [
            (cell[0], cell[1] + 1),
            (cell[0], cell[1] - 1),
            (cell[0] - 1, cell[1]),
            (cell[0] + 1, cell[1])
        ]

        open_neighbours = []
        wall_neighbours = []
        unknown_neighbours = []

        for i in range(4):
            if (neighbours[i] in self.open_list) or (neighbours[i] in self.oxygen_list):
                open_neighbours.append(i+1)
            elif neighbours[i] in self.wall_list:
                wall_neighbours.append(i+1)
            else:
                unknown_neighbours.append(i+1)

        return open_neighbours, wall_neighbours, unknown_neighbours

    def check_for_completion(self):
        for cell in self.open_list:
            unknown_neighbours = self.check_neighbours(cell)[2]
            if unknown_neighbours:
                return False

        else:
            return True

    def map_out_area(self, render_every=1, render_type='distance'):
        i = 0
        direction = 1
        while not self.check_for_completion():
            empty, wall, unknown = self.check_neighbours(self.position)

            # Always want a wall to the right
            forward = direction
            right = RIGHT_MAP[direction]
            left = LEFT_MAP[direction]
            back = LEFT_MAP[left]

            if right not in wall:
                direction_to_try = right
            elif forward not in wall:
                direction_to_try = forward
            elif left not in wall:
                direction_to_try = left
            else:
                direction_to_try = back

            status = self.step_on_input(direction_to_try)
            if status > 0:
                # Have moved and not hit a wall
                direction = direction_to_try


            if i % render_every == 0:
                self.render(type=render_type)
            i += 1

    def wall_grid(self):
        open = np.array(self.open_list)
        if self.wall_list:
            wall = np.array(self.wall_list)
        else:
            wall = np.zeros((0, 2), dtype=int)
        if self.oxygen_list:
            oxygen = np.array(self.oxygen_list)
        else:
            oxygen = np.zeros((0, 2), dtype=int)
        all_points = np.vstack((open, wall, oxygen))
        minima = np.min(all_points, axis=0)
        maxima = np.max(all_points, axis=0)
        grid = np.zeros((maxima - minima + 1), dtype=int)
        grid[open[:, 0] - minima[0], open[:, 1] - minima[1]] = 1
        grid[wall[:, 0] - minima[0], wall[:, 1] - minima[1]] = 0
        grid[oxygen[:, 0] - minima[0], oxygen[:, 1] - minima[1]] = 1
        return grid, -minima


def flood_fill(grid, origin, starting_index):
    distance = np.inf*np.ones_like(grid)
    distance[starting_index[0] + origin[0], starting_index[1]+origin[1]] = 0
    while True:
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if grid[i, j] == 0:
                    # wall
                    continue

                if not np.isinf(distance[i, j]):
                    # done
                    continue

                neighbours = np.inf*np.array([1, 1, 1, 1], dtype=float)
                if i == 0:
                    neighbours[0] = np.inf
                else:
                    neighbours[0] = float(distance[i-1, j])

                if i == grid.shape[0]-1:
                    neighbours[1] = np.inf
                else:
                    neighbours[1] = float(distance[i+1, j])

                if j == 0:
                    neighbours[2] = np.inf
                else:
                    neighbours[2] = float(distance[i, j-1])

                if j == grid.shape[1] - 1:
                    neighbours[3] = np.inf
                else:
                    neighbours[3] = float(distance[i, j+1])

                dist = np.min(neighbours)
                if not np.isinf(dist):
                    distance[i, j] = int(dist) + 1

        if not np.any(np.isinf(distance[grid > 0])):
            break

    distance[np.isinf(distance)] = -1
    return distance



if __name__ == "__main__":
    code = common.import_file('../input/day15')
    s = MapMaker(code)
    s.map_out_area(render_every=2000, render_type="none")
    common.part(1, s.oxy_distance[0])
    d = flood_fill(*s.wall_grid(), s.oxygen_list[0])
    common.part(2, int(np.max(d)))