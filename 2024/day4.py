import numpy as np

import common

with open("input/day4") as file:
    text = file.read()


# text = """MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX"""


as_array = common.convert_string_to_np_array(text, {"X": 1, "M": 2, "A": 3, "S": 4})

one_hot_array = np.zeros(as_array.shape + (4,), dtype=int)
for i, letter in enumerate("XMAS"):
    one_hot_array[:, :, i] = (as_array == (i+1))


base_kernel = np.eye(4)
kernels = [
    base_kernel[None, ...],
    base_kernel[:, None, :],
    base_kernel[::-1, None, :],
    base_kernel[None, ::-1, :],
]

fully_diag = np.zeros((4, 4, 4))
for i in range(4):
    fully_diag[i, i, i] = 1

kernels = kernels + [
    fully_diag,
    fully_diag[::-1, :, :],
    fully_diag[:, ::-1, :],
    fully_diag[::-1, ::-1, :],
]


matches = 0
for i_row in range(one_hot_array.shape[0]):
    for i_col in range(one_hot_array.shape[1]):
        for kernel in kernels:
            block = one_hot_array[i_row:i_row+kernel.shape[0], i_col:i_col+kernel.shape[1], :]
            if block.shape != kernel.shape:
                continue
            if (block * kernel).sum() == 4:
                matches += 1
                continue

print(f"Part 1: {matches}")


# --- PART 2

one_hot_array_2 = one_hot_array[..., 1:]
# base_kernel = np.eye(3)
# kernels = [
#     base_kernel[None, ...],
#     base_kernel[:, None, :],
#     base_kernel[::-1, None, :],
#     base_kernel[None, ::-1, :],
# ]

kernels = []
fully_diag = np.zeros((3, 3, 3))
for i in range(3):
    fully_diag[i, i, i] = 1

kernels = kernels + [
    fully_diag,
    fully_diag[::-1, :, :],
    fully_diag[:, ::-1, :],
    fully_diag[::-1, ::-1, :],
]
matches = 0
for i_row in range(one_hot_array_2.shape[0]):
    for i_col in range(one_hot_array_2.shape[1]):
        is_match = 0
        for kernel in kernels:
            block = one_hot_array_2[i_row:i_row+kernel.shape[0], i_col:i_col+kernel.shape[1], :]
            if block.shape != kernel.shape:
                continue
            if (block * kernel).sum() == 3:
                is_match += 1

            if is_match == 2:
                is_match += 1  # don't hit again
                matches += 1
                continue

print(f"Part 2: {matches}")