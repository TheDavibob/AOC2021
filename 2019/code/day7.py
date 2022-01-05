import itertools

import common
from intcode import run_intcode, Intcode


def try_all_possibilities(intcode):
    default = [0, 1, 2, 3, 4]
    permutations = itertools.permutations(default)
    best = 0
    for p in permutations:
        output = 0
        for j in range(5):
            output = run_intcode(intcode, [p[j], output])[1][0]

        if output > best:
            best = output

    return best


def try_possibility_with_feedback(permutation, intcode):
    machines = [Intcode(intcode, [permutation[i]], pause_on_no_inputs=True) for i in range(5)]
    machines[0].input_list.append(0)

    finished = False
    while not finished:
        for i in range(4):
            machines[i].step_all()
            machines[i+1].input_list += machines[i].output_list
            machines[i].output_list = []

        status = machines[4].step_all()
        if status == 0:
            finished = True
            output = machines[4].output_list[-1]
        else:
            machines[0].input_list += machines[4].output_list
            machines[4].output_list = []

    return output


def try_all_possibilities_with_feedback(intcode):
    default = [5, 6, 7, 8, 9]
    permutations = itertools.permutations(default)
    best = 0
    for p in permutations:
        output = try_possibility_with_feedback(p, intcode)
        if output > best:
            best = output

    return best


if __name__ == "__main__":
    intcode = common.import_file("../input/day7")
    print(try_all_possibilities(intcode))
    print(try_all_possibilities_with_feedback(intcode))