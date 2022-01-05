import time

import numpy as np
from copy import copy

import common


POSSIBLE_ROLLS = []
for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                for m in range(3):
                    for n in range(3):
                        POSSIBLE_ROLLS.append((i+1, j+1, k+1, l+1, m+1, n+1))


POSSIBLE_TRIPLES = []
for i in range(3):
    for j in range(3):
        for k in range(3):
            POSSIBLE_TRIPLES.append((i+1, j+1, k+1))


class DiceGame:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

        self.score_1 = 0
        self.score_2 = 0

        self.counter = 1

    def step(self, target):
        finished = False
        for _ in range(3):
            roll = (self.counter - 1) % 10 + 1
            self.p1 += roll
            if self.p1 >= 11:
                self.p1 = (self.p1 - 1) % 10 + 1
            self.counter += 1

        self.score_1 += self.p1
        if self.score_1 >= target:
            print(f"Player 1 wins! {self.score_2 * (self.counter-1)}")
            finished = True
            return finished

        for _ in range(3):
            roll = (self.counter - 1) % 10 + 1
            self.p2 += roll
            if self.p2 >= 11:
                self.p2 = (self.p2 - 1) % 10 + 1
            self.counter += 1

        self.score_2 += self.p2
        if self.score_2 >= target:
            print(f"Player 2 wins! {self.score_1 * (self.counter-1)}")
            finished = True
            return finished

        return finished

    def step_all(self, target):
        finished = False
        while not finished:
            finished = self.step(target)


class NTurns:
    def __init__(self, init_position):
        self.score_pos_grid = [[0 for _ in range(21)] for _ in range(10)]
        self.score_pos_grid[init_position-1][0] = 1

    def iterate(self):
        newly_finished = 0
        new_grid = [[0 for _ in range(21)] for _ in range(10)]
        for i in range(10):
            for j in range(21):
                if self.score_pos_grid[i][j] == 0:
                    continue

                count = self.score_pos_grid[i][j]

                for delta, weight in zip([3, 4, 5, 6, 7, 8, 9], [1, 3, 6, 7, 6, 3, 1]):
                    new_i = (i + delta) % 10
                    new_j = j + new_i + 1
                    if new_j >= 21:
                        newly_finished += weight*count
                    else:
                        new_grid[new_i][new_j] += weight*count

        self.score_pos_grid = new_grid
        return newly_finished

    def not_finished(self):
        count = 0
        for i in range(10):
            for j in range(21):
                count += self.score_pos_grid[i][j]
        return count


def two_grids(pos1, pos2):
    grid_1 = NTurns(pos1)
    grid_2 = NTurns(pos2)

    winning_1 = 0
    winning_2 = 0

    finished_2, not_finished_2 = 0, 0
    while True:
        finished_1 = grid_1.iterate()
        not_finished_1 = grid_1.not_finished()
        winning_1 += finished_1 * not_finished_2

        finished_2 = grid_2.iterate()
        not_finished_2 = grid_2.not_finished()

        winning_2 += finished_2 * not_finished_1

        if (not_finished_1 == 0) and (not_finished_2 == 0):
            break

    return winning_1, winning_2


if __name__ == "__main__":
    game = DiceGame(8, 2)
    print("Part 1:")
    game.step_all(1000)

    print(f"Part 2: {max(two_grids(8, 2))}")
