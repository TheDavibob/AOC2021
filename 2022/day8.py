import numpy as np
import common


def input_to_array(text):
    array = np.zeros((len(text.split("\n")[0]), len(text.split("\n"))-1), dtype=int)
    for i, line in enumerate(text.split("\n")[:-1]):
        for j, char in enumerate(line):
            array[i, j] = int(char)

    return array


def is_visible(array, i, j):
    target = array[i, j]
    if np.all(target > array[:i, j]):
        return True
    elif np.all(target > array[i+1:, j]):
        return True
    elif np.all(target > array[i, :j]):
        return True
    elif np.all(target > array[i, j+1:]):
        return True
    else:
        return False


def count_visible(array):
    count = 0
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            count += is_visible(array, i, j)

    return count


def scenic_score(array, i, j):
    trees_up = array[:i, j][::-1]
    trees_down = array[(i+1):, j]
    trees_left = array[i, :j][::-1]
    trees_right = array[i, (j+1):]

    start_value = array[i, j]

    return view_length(trees_up, start_value) * view_length(trees_left, start_value) * view_length(trees_down, start_value) * view_length(trees_right, start_value)


def view_length(one_d_array, start_value):
    i = -1
    for i, char in enumerate(one_d_array):
        if char >= start_value:
            break

    return i+1


def highest_scenic_score(array):
    ss = np.zeros_like(array)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            ss[i, j] = scenic_score(array, i, j)

    return np.max(ss), ss


test_text = """30373
25512
65332
33549
35390
"""


if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    array = input_to_array(text)

    common.part(1, count_visible(array))

    # array = input_to_array(test_text)
    # print(highest_scenic_score(array)[1])

    common.part(2, highest_scenic_score(array)[0])
