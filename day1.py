import numpy as np
import common

text = common.import_file("input/day1_input")
ints = common.return_int_list(text)

"""
PART 1
"""
print(f"Part 1: {np.sum(np.diff(ints) > 0)}")

"""
PART 2
"""
# Brute force combination of rolling average
sliding_window = ints[2:] + ints[:-2] + ints[1:-1]
print(f"Part 2: {np.sum(np.diff(sliding_window) > 0)}")
