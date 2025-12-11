# /// script
# dependencies = [
#   "numpy>=2.0.0",
#   "tqdm"
# ]
# ///
import itertools
from idlelib.rpc import pickle_code

import numpy as np
from tqdm import tqdm


TEST_INPUT = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""


with open("data/day_10") as f:
    REAL_DATA = f.read()

def step(
        states_dict,
        flips,
        costs
):
    updated = False
    new_state_dict = states_dict.copy()
    for state, cost_so_far in states_dict.items():
        for flip, cost in zip(flips, costs):
            new_state = apply_flip(state, flip)
            new_cost = cost + cost_so_far
            if new_state in states_dict:
                if new_cost < states_dict[new_state]:
                    new_state_dict[new_state] = new_cost
                    updated = True
            else:
                new_state_dict[new_state] = new_cost
                updated = True

    return updated, new_state_dict


def apply_flip(state, flip):
    new_state = list(state)
    for idx in flip:
        new_state[idx] = not state[idx]
    return tuple(new_state)


def get_cost(target_state, flips, costs, single_cost: bool = False):
    if single_cost:
        costs = [1 for f in flips]

    start_state = tuple(False for s in target_state)
    updated = True
    state_dict = {start_state: 0}

    while updated:
        updated, state_dict = step(state_dict, flips, costs)
        if target_state in state_dict:
            break

    return state_dict[target_state]


def parse_line(puzzle_line):
    start, rest = puzzle_line.split("] ")
    state_str = start[1:]
    target = []
    for s in state_str:
        if s == ".":
            target.append(False)
        else:
            target.append(True)

    target = tuple(target)

    mid, end = rest.split(" {")
    cost_str = end[:-1]
    costs = []
    for val in cost_str.split(","):
        costs.append(int(val))

    flips = mid.split(" ")
    all_flips = []
    for f in flips:
        this_flip = []
        for g in f[1:-1].split(","):
            this_flip.append(int(g))
        all_flips.append(this_flip)

    return target, all_flips, costs


def part_one(puzzle_input):
    total = 0
    for line in puzzle_input.split("\n"):
        t, f, c = parse_line(line)
        total += get_cost(t, f, c, single_cost=True)

    return total


def step_2(
    states_dict,
    flips,
    iteration,
    target_state,
):
    new_state_dict = states_dict.copy()
    new_things = 0
    for state, cost_so_far in states_dict.items():
        if cost_so_far != iteration - 1:
            continue

        for flip in flips:
            new_state = apply_joltage(state, flip)

            if new_state in states_dict:
                continue
            elif any(s > t for s, t in zip(new_state, target_state)):
                continue
            else:
                new_state_dict[new_state] = iteration
                new_things += 1

    return new_state_dict


def apply_joltage(state, flip):
    new_state = list(state)
    for idx in flip:
        new_state[idx] = state[idx] + 1
    return tuple(new_state)


def get_cost_2(target_joltage, flips):
    target_joltage = tuple(target_joltage)

    start_state = tuple(0 for s in target_joltage)
    state_dict = {start_state: 0}

    for iteration in tqdm(range(1, sum(target_joltage))):
        state_dict = step_2(state_dict, flips, iteration, target_joltage)
        if target_joltage in state_dict:
            break

    return state_dict[target_joltage]


def part_two(puzzle_input):
    total = 0
    lines = puzzle_input.split("\n")
    for i_line, line in enumerate(lines):
        print(f"Tackling {i_line} of {len(lines)}")
        t, f, c = parse_line(line)
        total += get_cost_2(c, f)

    return total


def get_all_options(target, flips):
    flip_arrays = []
    for flip in flips:
        array = np.zeros(len(target), dtype=int)
        for i in flip:
            array[i] = 1
        flip_arrays.append(array)

    equation_size = np.sum(flip_arrays, axis=0)
    n_state = len(target)
    n_dof = len(flips)
    # print(n_state, n_dof, equation_size)

    flip_array = np.array(flip_arrays, dtype=float).T
    target_array = np.array(target, dtype=float)

    old_array = flip_array.copy()
    unchanged = False
    while not unchanged:
        flip_array, target_array = rearrange_to_diagonalish(flip_array, target_array)
        flip_array, target_array = reduce(flip_array, target_array)

        unchanged = np.all(flip_array == old_array)
        old_array = flip_array.copy()

    # print(flip_array, target)
    # Pretty sure this has worked, but now need to back out the solution
    # subspace from tihs...

    # Coefficients are "arbitrary" if they are either on a diagonal element
    # that is zero, or are to the right of the final diagonal
    arbitrary_cmpts = []

    for i in range(min(*flip_array.shape)):
        if flip_array[i, i] == 0:
            arbitrary_cmpts.append(i)

    if flip_array.shape[1] > flip_array.shape[0]:
        for i in range(flip_array.shape[0], flip_array.shape[1]):
            arbitrary_cmpts.append(i)

    cmpt_ranges = []
    for cmpt in arbitrary_cmpts:
        this_flip = flip_arrays[cmpt].astype(bool)
        max_count = int(min(np.array(target)[this_flip])) + 1
        cmpt_ranges.append(max_count)

    valid_range = []
    for cmpt in range(flip_array.shape[1]):
        this_flip = flip_arrays[cmpt].astype(bool)
        max_count = int(min(np.array(target)[this_flip])) + 1
        valid_range.append(max_count)

    best_so_far = np.inf
    best_weights = None
    invalid_tails = set()

    for range_to_try in tqdm(
            itertools.product(*[range(c) for c in cmpt_ranges]),
            total=np.prod(cmpt_ranges)
    ):
        skip = False
        for i in range(len(range_to_try)):
            idx = -i-1
            if range_to_try[idx:] in invalid_tails:
                skip = True
                continue
        if skip:
            continue

        if np.sum(range_to_try) > best_so_far:
            continue
        nominal_weights, invalid_tail = extract_from_ge_reduced(
            flip_array,
            target_array,
            arbitrary_cmpts,
            np.array(range_to_try),
            valid_range,
        )
        if nominal_weights is None:
            invalid_tails.add(tuple(invalid_tail))
            continue
        if np.sum(nominal_weights) >= best_so_far:
            continue
        if np.any(nominal_weights < 0):
            continue
        if np.any(nominal_weights > valid_range):
            continue

        if np.all(np.isclose(
            np.einsum("i,ji->j", nominal_weights, flip_array),
            target_array
        )):
                best_so_far = np.sum(nominal_weights)
                best_weights = nominal_weights

    return int(np.round(best_so_far)), best_weights


def extract_from_ge_reduced(A, y, fixed_idx, fixed_vals, upper_bound):
    weights_array = np.nan*np.zeros(A.shape[1])
    for i_idx, idx in enumerate(fixed_idx):
        weights_array[idx] = fixed_vals[i_idx]

    while np.any(np.isnan(weights_array)):
        for idx in range(1, A.shape[1]+1):
            if np.isnan(weights_array[-idx]):
                this_idx = A.shape[1] - idx
                break

        weights_array[this_idx] = (
            y[this_idx]
            - np.dot(A[this_idx, this_idx+1:], weights_array[this_idx+1:])
        )

        if weights_array[this_idx] < 0:
            return None, [f for f in fixed_idx if f > this_idx]

        if weights_array[this_idx] > upper_bound[this_idx]:
            return None, [f for f in fixed_idx if f > this_idx]

        if not np.isclose(weights_array[this_idx], np.round(weights_array[this_idx])):
            return None, [f for f in fixed_idx if f > this_idx]

    return weights_array, None


def swap_rows(A, y, i, j):
    new_A = A.copy()
    new_A[i] = A[j]
    new_A[j] = A[i]

    new_y = y.copy()
    new_y[i] = y[j]
    new_y[j] = y[i]
    return new_A, new_y


def subtract_multiple_of_row(A, y, i, j, alpha):
    new_A = A.copy()
    new_A[i] = A[i] - alpha * A[j]

    new_y = y.copy()
    new_y[i] = y[i] - alpha * y[j]
    return new_A, new_y


def multiply_row(A, y, i, alpha):
    new_A = A.copy()
    new_y = y.copy()

    new_A[i] = alpha * A[i]
    new_y[i] = alpha * y[i]
    return new_A, new_y


def rearrange_to_diagonalish(A, y):
    done = False
    while not done:
        done = True
        for col in range(A.shape[1]):
            if (A[col:, col] != 0).sum() == 1:
                if A[col, col] == 0:
                    for row in range(col, A.shape[0]):
                        if A[row, col] != 0:
                            this_row = row
                            this_col = col
                            done = False
                            break

        if not done:
            A, y = swap_rows(A, y, this_col, this_row)

    done = True
    for col in range(A.shape[1]):
        if (A[col:, col] != 0).sum() > 1:
            if A[col, col] == 0:
                for row in range(col, A.shape[0]):
                    if A[row, col] != 0:
                        done = False
                        this_row = row
                        this_col = col

    if not done:
        A, y = swap_rows(A, y, this_col, this_row)

    for col in range(A.shape[1]):
        if col < A.shape[0]:
            if A[col, col] == 0:
                continue
            A, y = multiply_row(A, y, col, 1 / A[col, col])

    return A, y


def reduce(A, y):
    # Assumed put into neat form, above
    for col in range(A.shape[1]):
        if (A[col:, col] != 0).sum() > 1 and A[col, col] != 0:
            # Can reduce this row
            for row in range(col+1, A.shape[0]):
                A, y = subtract_multiple_of_row(A, y, row, col, A[row, col] / A[col, col])

            break
    return A, y


if __name__ == "__main__":
    assert part_one(TEST_INPUT) == 7
    print(f"Part 1: {part_one(REAL_DATA)}")

    # assert part_two(TEST_INPUT) == 33
    # print(f"Part 2: {part_two(REAL_DATA)}")

    total = 0
    lines = REAL_DATA.split("\n")
    for i_line, line in enumerate(lines):
        _, f, t = parse_line(line)
        new, weights = get_all_options(t, f)
        total += new
        #19560 is too low
        #19568 is too low
        #19576 is too high

        #19572 is wrong
        #19573 is wrong
        # 19574 is right? I overcounted by just 2

        print(f"{i_line} of {len(lines)}", total)
        print(f"new count: {new}, weights: {weights}")