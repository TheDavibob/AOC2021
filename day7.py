import numpy as np

import common

def triangle(n):
    """
    Sum of first n numbers
    """
    n = abs(n)
    return n*(n+1)//2


def minimise_over_potential_positions(positions, norm):
    stored_delta = np.sum(triangle(positions - min(positions)))

    for trial_position in range(min(positions), max(positions)):
        delta = np.sum(norm(positions - trial_position))
        if delta < stored_delta:
            stored_delta = delta

    return stored_delta


if __name__ == "__main__":
    text = common.import_file('input/day7_input')
    pos = np.array([int(t) for t in text.split(',')])

    print(f"Part 1: {minimise_over_potential_positions(pos, np.abs)}")
    print(f"Part 2: {minimise_over_potential_positions(pos, triangle)}")