import numpy as np
from matplotlib import pyplot as plt

import common
import intcode


def initial_render(int_list):
    each_coord = np.reshape(int_list, (-1, 3))
    score = each_coord[each_coord[:, 0] == -1, 2]
    if len(score) > 0:
        score = score[0]
    else:
        score = None
    each_coord = each_coord[each_coord[:, 0] >= 0]
    grid = np.zeros((each_coord[-1][1]+1, each_coord[-1][0] + 1), dtype=int)
    grid[each_coord[:, 1], each_coord[:, 0]] = each_coord[:, 2]
    plot = plt.matshow(grid)
    plt.draw()
    plt.pause(0.01)


    return plot, grid, score


def get_best_movement(grid):
    ball_x = np.where(grid == 4)[1][0]
    paddle_x = np.where(grid == 3)[1][0]
    if paddle_x < ball_x:
        return 1
    elif paddle_x == ball_x:
        return 0
    else:
        return -1


def subsequent_render(plot, grid, int_list, render=True):
    each_coord = np.reshape(int_list, (-1, 3))
    score = each_coord[each_coord[:, 0] == -1, 2]
    if len(score) > 0:
        score = score[0]
    else:
        score = None
    each_coord = each_coord[each_coord[:, 0] >= 0]
    grid[each_coord[:, 1], each_coord[:, 0]] = each_coord[:, 2]
    if render:
        plot.set_data(grid)
        plt.draw()
        plt.pause(0.01)
    return score


def play_game(code, render_every=1, verbose=True):
    int_code = [int(s) for s in code.split(',')]
    int_code[0] = 2
    s = intcode.Intcode(int_code, pause_on_no_inputs=True)
    s.step_all()
    plot, grid, score = initial_render(s.output_list)
    if verbose:
        print(score)
    s.output_list = []

    #new_input = input("Enter -1, 0, or 1")
    s.input_list.append(get_best_movement(grid))

    finished = False
    i = 1
    best_score = 0
    while not finished:
        output_code = s.step_all()
        render = (i % render_every) == 0
        score = subsequent_render(plot, grid, s.output_list, render)
        if score:
            best_score = score
            if verbose:
                print(score)
        s.output_list = []

        if output_code == 0:
            finished = True
        else:
            # new_input = input("Enter -1, 0, or 1")
            s.input_list.append(get_best_movement(grid))

        i += 1

    return best_score


if __name__ == "__main__":
    code = common.import_file('../input/day13')
    input_str = intcode.run_intcode(code)[-1]
    coord_list = np.reshape(input_str, (-1, 3))
    common.part(1, np.sum(coord_list[:, 2] == 2))
    common.part(2, play_game(code, render_every=20000, verbose=False))
    # Fun can be had by putting render down to something sensible, even e.g. 1
