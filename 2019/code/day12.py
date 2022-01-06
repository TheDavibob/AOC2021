from math import lcm

import numpy as np
import common


def parse_input(text):
    planets = []
    for line in text.split('\n'):
        if line == "":
            continue

        line = line.replace("<", "")
        line = line.replace(">", "")
        line = line.replace(" ", "")
        coords = []
        for c in line.split(","):
            coords.append(int(c.split("=")[-1]))

        planets.append(coords)

    return np.array(planets, dtype=int)


class SingleColumn:
    def __init__(self, column):
        self.planets = column
        self.velocity = np.zeros(4, dtype=int)

    def step(self):
        for i in range(4):
            self.velocity[i] += np.sum(self.planets[i] < self.planets) - np.sum(self.planets[i] > self.planets)

        self.planets += self.velocity


class ThreeColumns:
    def __init__(self, planets):
        self.columns = [SingleColumn(planets[:, i]) for i in range(3)]

    def step(self):
        for column in self.columns:
            column.step()

    def get_positions_and_velocities(self):
        velocities = np.vstack([column.velocity for column in self.columns])
        positions = np.vstack([column.planets for column in self.columns])
        return positions, velocities

    def get_energy(self):
        positions, velocities = self.get_positions_and_velocities()
        kinetic_energy = np.sum(np.abs(velocities), axis=0)
        potential_energy = np.sum(np.abs(positions), axis=0)

        return np.sum(kinetic_energy * potential_energy)


def calculate_restart(single_column: SingleColumn):
    initial_position = single_column.planets.copy()
    initial_velocity = single_column.velocity.copy()

    i = 1
    while True:
        single_column.step()
        if np.all(single_column.planets == initial_position) and np.all(single_column.velocity == initial_velocity):
            break
        i += 1

    return i


def calculate_all_restart(three_columns: ThreeColumns):
    individual_cycles = []
    for i in range(3):
        individual_cycles.append(calculate_restart(three_columns.columns[i]))

    return lcm(*individual_cycles)


if __name__ == "__main__":
    text = common.import_file("../input/day12")
    planets = parse_input(text)

    c = ThreeColumns(planets)
    for i in range(1000):
        c.step()
    common.part(1, c.get_energy())

    c = ThreeColumns(parse_input(text))
    common.part(2, calculate_all_restart(c))