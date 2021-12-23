from copy import copy, deepcopy

import numpy as np
import common
import networkx

BIN_MAP = {s: i for s, i in zip(('A', 'B', 'C', 'D'), range(4))}
COST_MAP = {s: 10**i for s, i in zip(('A', 'B', 'C', 'D'), range(4))}
INVERSE_MAP = {i: s for s, i in BIN_MAP.items()}
OUTER_STATE_MAP = {
    i: j for i, j in zip(range(7), (0, 1, 3, 5, 7, 9, 10))
}


def argsort(seq):
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=seq.__getitem__)


def parse_input(text):
    lines = [line for line in text.split('\n') if line != ""]
    a = [lines[2][3], lines[3][3]]
    b = [lines[2][5], lines[3][5]]
    c = [lines[2][7], lines[3][7]]
    d = [lines[2][9], lines[3][9]]

    return a, b, c, d


class State:
    def __init__(self, A, B, C, D):
        self.bin = [copy(s) for s in (A, B, C, D)]
        self.outer = [None for _ in range(7)]
        self.total_cost = 0

    def get_possibilities(self):
        open = [False, False, False, False]
        viable_moves = []
        costs = []
        for i in range(4):
            if len(self.bin[i]) > 0:
                if all([element == INVERSE_MAP[i] for element in self.bin[i]]):
                    open[i] = True
                else:
                    head = self.bin[i][0]
                    viable = get_viable_moves(self.outer, i+2)
                    for v in viable:
                        viable_moves.append(
                            ('out', i, v, head)
                        )
                        costs.append(calc_cost_delta(i, head, v))
            else:
                open[i] = True

        for i, out in enumerate(self.outer):
            if out is None:
                continue

            # out is one of 'A', 'B', 'C', 'D'
            target_bin = BIN_MAP[out]

            # Can move to target bin if:
            # - bin is empty
            # - all spaces to bin are empty

            if not open[target_bin]:
                continue

            possible = True
            if target_bin + 2 < i:
                start = target_bin + 2
                end = copy(i)
            else:
                start = i+1
                end = target_bin + 2

            for j in range(start, end):
                if self.outer[j]:
                    possible = False
                    break

            if possible:
                viable_moves.append(
                    ('in', i, target_bin, out)
                )
                costs.append(0)

        order = argsort(costs)

        return [viable_moves[i] for i in order], sorted(costs)

    def progress_possibility(self, possibility, cost):
        self.total_cost += cost
        if possibility[0] == 'out':
            self.outer[possibility[2]] = possibility[3]
            self.bin[possibility[1]].pop(0)
        else:
            self.bin[possibility[2]].append(possibility[3])
            self.outer[possibility[1]] = None

    def is_finished(self):
        if not all(o is None for o in self.outer):
            return False

        for i in range(4):
            if not all([element == INVERSE_MAP[i] for element in self.bin[i]]):
                return False

        return True


def get_viable_moves(outer, split):
    try:
        min_index = next(i for i, o in enumerate(outer[split-1::-1]) if o is not None)
        minimum_blocker = split - 1 - min_index
    except StopIteration:
        minimum_blocker = -1

    try:
        maximum_blocker = next(i+split for i, o in enumerate(outer[split:]) if o is not None)
    except StopIteration:
        maximum_blocker = len(outer)

    return [i for i in range(minimum_blocker+1, maximum_blocker)]


def calc_cost_delta(initial_bin, type, outer_state):
    target_bin = BIN_MAP[type]

    if target_bin < initial_bin:
        smallest, largest = target_bin, initial_bin
    else:
        smallest, largest = initial_bin, target_bin

    outer_fine_state = OUTER_STATE_MAP[outer_state]
    smallest_fine_bin = 2*smallest + 2
    largest_fine_bin = 2*largest + 2

    if outer_fine_state < smallest_fine_bin:
        cost_delta = smallest_fine_bin - outer_fine_state
    elif outer_fine_state > largest_fine_bin:
        cost_delta = outer_fine_state - largest_fine_bin
    else:
        cost_delta = 0

    return int(2*cost_delta*COST_MAP[type])


class TryAllPossibilities:
    def __init__(self, initial_state: State):
        self.state_history = [deepcopy(initial_state)]
        self.command_history = [0]
        self.possibility_history = []
        self.cost_history = []
        self.successful_command = None
        self.best_cost = 1000000

    def step(self):
        possibilities, costs = self.state_history[-1].get_possibilities()
        print(self.best_cost, len(possibilities), self.command_history)
        if self.state_history[-1].is_finished():
            # Store
            if self.state_history[-1].total_cost < self.best_cost:
                self.successful_command = (deepcopy(self.possibility_history))
                self.best_cost = self.state_history[-1].total_cost

            # Back up
            self.state_history = self.state_history[:-1]
            self.command_history = self.command_history[:-1]
            self.possibility_history = self.possibility_history[:-1]
            if len(self.command_history) == 0:
                return True
            self.command_history[-1] += 1
        elif (self.command_history[-1] == len(possibilities)) or (self.state_history[-1].total_cost >= self.best_cost):
            # Back up
            self.state_history = self.state_history[:-1]
            self.command_history = self.command_history[:-1]
            self.possibility_history = self.possibility_history[:-1]
            if len(self.command_history) == 0:
                return True
            self.command_history[-1] += 1
        else:
            possibility = possibilities[self.command_history[-1]]
            cost = costs[self.command_history[-1]]
            state = deepcopy(self.state_history[-1])
            state.progress_possibility(possibility, cost)
            self.state_history.append(deepcopy(state))
            self.command_history.append(0)
            self.possibility_history.append(possibility)

        return False

    def step_all(self):
        finished = False
        while not finished:
            finished = self.step()


def get_baseline(state: State):
    initial_states = state.bin
    n_per_state = len(initial_states[0])
    cost = 0
    for i in range(len(state.bin)):
        for j in range(n_per_state):
            state = initial_states[i][j]
            target_bin = BIN_MAP[state]
            new_cost = 2*abs(target_bin - i)
            exit_cost = (j+1)
            cost += (exit_cost + new_cost) * COST_MAP[state]

            if (new_cost == 0) and j == (n_per_state - 1):
                cost -= 2*exit_cost*COST_MAP[state]

    entry_cost = n_per_state * (n_per_state + 1) // 2
    for state in ('A', 'B', 'C', 'D'):
        cost += entry_cost * COST_MAP[state]
    return cost

if __name__ == "__main__":
    text = common.import_file('input/day23_input')
    a, b, c, d = parse_input(text)
    # s = State(a, b, c, d)
    # baseline_cost = get_baseline(s)
    # t = TryAllPossibilities(s)
    # t.step_all()
    # print(t.best_cost + baseline_cost)

    s = State(
        [a[0], 'D', 'D', a[1]],
        [b[0], 'C', 'B', b[1]],
        [c[0], 'B', 'A', c[1]],
        [d[0], 'A', 'C', d[1]],
    )
    baseline_cost = get_baseline(s)
    t = TryAllPossibilities(s)
    t.step_all()
    print(t.best_cost + baseline_cost)