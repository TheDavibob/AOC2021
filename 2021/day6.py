import numpy as np

import common


def increment(state: np.array):
    # the slow approach
    new_fish = np.sum(state == 0)

    new_state = np.concatenate((state, 9*np.ones(new_fish)))
    new_state[new_state == 0] = 7
    new_state -= 1

    return new_state


def update_counts(counts):
    # the fast approach
    new_counts = np.zeros_like(counts)
    new_counts[:-1] = counts[1:]
    new_counts[6] += counts[0]
    new_counts[8] += counts[0]
    return new_counts


if __name__ == "__main__":
    text = common.import_file('input/day6_input')
    initial_state = [int(s) for s in text.split(',')]

    state = np.array(initial_state)
    for _ in range(80):
        state = increment(state)

    print(f"Part 1: {len(state)}")

    counts = np.histogram(initial_state, np.arange(10))[0]
    for _ in range(256):
        counts = update_counts(counts)

    print(f"Part 2: {np.sum(counts)}")
