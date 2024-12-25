import numpy as np

import common


def parse_input(text):
    keys = []
    locks = []

    for block in text.split("\n\n"):
        as_array = common.convert_string_to_np_array(block, {".": 0, "#": 1})
        if np.all(as_array[0]):
            locks.append(as_array)
        else:
            keys.append(as_array)
    return keys, locks


def test_pair_valid(key, lock):
    return not np.any((key + lock) >= 2)


def count_valid_combos(keys, locks):
    valid = 0
    for key in keys:
        for lock in locks:
            if test_pair_valid(key, lock):
                valid += 1

    return valid


if __name__ == "__main__":
    with open("input/day25") as file:
        text = file.read()

    keys, locks = parse_input(text)
    print(count_valid_combos(keys, locks))