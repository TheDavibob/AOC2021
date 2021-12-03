import numpy as np

import common

text = common.import_file('input/day3_input')
text = common.convert_string_to_np_array(text, {"0": 0, "1": 1})


def from_binary(bool_array):
    return np.sum(2**np.arange(len(bool_array))[::-1] * bool_array)


gamma = from_binary(np.sum(text, axis=0) > 500)
epsilon = from_binary(np.sum(text, axis=0) < 500)

print(gamma * epsilon)


def reduce_to_single_value(array, type='oxy'):
    new_array = array.copy()
    counter = 0
    while len(new_array) > 1:
        switch = np.sum(new_array[:, counter]) >= len(new_array) / 2
        if type == 'oxy':
            pass
        elif type == 'co2':
            switch = not switch

        if switch:
            new_array = new_array[new_array[:, counter] == 1]
        else:
            new_array = new_array[new_array[:, counter] == 0]
        counter += 1
        counter %= new_array.shape[1]

    return new_array[0]


o = reduce_to_single_value(text, 'oxy')
c = reduce_to_single_value(text, 'co2')
print(from_binary(o) * from_binary(c))