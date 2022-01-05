import numpy as np
import common

def process_input(text):
    binary_string, map = text.split('\n\n')
    initial_map = common.convert_string_to_np_array(map, {".": 0, "#": 1})
    initial_map = initial_map.astype(bool)
    without_lines = binary_string.replace("\n", "")
    with_ones = without_lines.replace("#", "1")
    with_zeros = with_ones.replace(".", "0")
    return with_zeros, initial_map


def iterate(map, binary_string, is_even):
    if is_even:
        extended_map = np.zeros((map.shape[0] + 4, map.shape[1] + 4), dtype=bool)
    else:
        extended_map = np.ones((map.shape[0] + 4, map.shape[1] + 4), dtype=bool)
    extended_map[2:-2, 2:-2] = map

    new_map = np.zeros((map.shape[0] + 2, map.shape[1] + 2), dtype=bool)
    for i in range(new_map.shape[0]):
        for j in range(new_map.shape[1]):
            square = extended_map[i:i+3, j:j+3]
            square_string = "".join([str(int(s)) for s in square.flatten()])
            # print(square_string, int(square_string, 2), int(binary_string[int(square_string, 2)]), (i, j))
            new_map[i, j] = int(binary_string[int(square_string, 2)])

    return new_map


if __name__ == "__main__":
    text = common.import_file("input/day20_input")
    # text = common.import_file("input/day20_test")
    binary_string, map = process_input(text)
    stored = map.copy()
    for i in range(25):
        map = iterate(map, binary_string, True)
        map = iterate(map, binary_string, False)
        print(f"Lights after {2*(i+1)} iterations: {np.sum(map)}")
