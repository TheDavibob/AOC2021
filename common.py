import numpy as np


def convert_string_to_np_array(input_string: str, mapping_dict: dict=None):
    lines = [line for line in input_string.split('\n') if line != '']

    len_line = len(lines[0])
    for line in lines:
        assert len(line) == len_line, 'Not all the lines are the same length'

    out_array = np.zeros((len(lines), len_line), dtype=int)

    character_list = set(''.join(lines))
    if mapping_dict is None:
        mapping_dict = {}
        for i_char, char in enumerate(character_list):
            mapping_dict[char] = i_char
    else:
        # Fill up mapping dict with any missing characters
        new_val = 0
        for char in character_list:
            if char in mapping_dict.keys():
                continue

            while new_val in mapping_dict.values():
                new_val += 1

            mapping_dict[char] = new_val

    for row, line in enumerate(lines):
        for column, character in enumerate(line):
            out_array[row, column] = mapping_dict[character]

    return out_array


def return_int_list(string):
    return np.array([int(num) for num in string.split('\n') if num != ''])


def import_file(filepath):
    with open(filepath) as file:
        text = file.read()

    return text
