import numpy as np
from matplotlib import pyplot as plt

import common


def step(line, signal_strength, register, n_cycle):
    if line == "noop":
        if (n_cycle - 20) % 40 == 0:
            signal_strength += n_cycle * register
        n_cycle += 1
    elif line.split(" ")[0] == "addx":
        n_add = int(line.split(" ")[1])

        if (n_cycle - 20) % 40 == 0:
            signal_strength += n_cycle * register
        n_cycle += 1

        if (n_cycle - 20) % 40 == 0:
            signal_strength += n_cycle * register
        n_cycle += 1

        register += n_add

    return signal_strength, register, n_cycle


def step_2(line, signal_strength, register, n_cycle, image):
    if line == "noop":
        if (n_cycle - 20) % 40 == 0:
            signal_strength += n_cycle * register
        red_n = n_cycle % 40
        if register in [red_n, red_n-1, red_n-2]:
            image[n_cycle-1] = 1
        else:
            image[n_cycle-1] = 0
        n_cycle += 1
    elif line.split(" ")[0] == "addx":
        n_add = int(line.split(" ")[1])

        if (n_cycle - 20) % 40 == 0:
            signal_strength += n_cycle * register
        red_n = n_cycle % 40
        if register in [red_n, red_n-1, red_n-2]:
            image[n_cycle-1] = 1
        else:
            image[n_cycle-1] = 0
        n_cycle += 1

        if (n_cycle - 20) % 40 == 0:
            signal_strength += n_cycle * register
        red_n = n_cycle % 40
        if register in [red_n, red_n-1, red_n-2]:
            image[n_cycle-1] = 1
        else:
            image[n_cycle-1] = 0
        n_cycle += 1

        register += n_add

    return signal_strength, register, n_cycle, image


test_instructions = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""


if __name__ == "__main__":
    text = common.load_todays_input(__file__)

    signal_strength = 0
    register = 1
    n_cycle = 1

    for line in text.split("\n"):
        if line == "":
            continue

        signal_strength, register, n_cycle = step(line, signal_strength, register, n_cycle)
        print(line + f" signal strength: {signal_strength}, register: {register}, cycle: {n_cycle}")

    common.part(1, signal_strength)

    # text = test_instructions
    signal_strength = 0
    register = 1
    n_cycle = 1
    image = np.zeros(6*40, dtype=int)

    for line in text.split("\n"):
        if line == "":
            continue

        signal_strength, register, n_cycle, image = step_2(line, signal_strength, register, n_cycle, image)

        print(image[40*(n_cycle//40):40+40*(n_cycle//40)])

    plt.matshow(image.reshape(6, 40))
    plt.show()

    common.part(2, "TBC")
