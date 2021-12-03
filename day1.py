import numpy as np
import common

text = common.import_file("input/day1_input")
print(np.sum(np.diff(common.return_int_list(text)) > 0))

ints = common.return_int_list(text)

sliding_window = ints[2:] + ints[:-2] + ints[1:-1]
print(np.sum(np.diff(sliding_window) > 0))