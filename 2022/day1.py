import numpy as np
import common

if __name__ == "__main__":
    text = common.import_file("input/day1")

    max_so_far = 0
    sum_so_far = 0
    for line in text.split("\n"):
        if line != "":
            sum_so_far += int(line)
        else:
            if sum_so_far > max_so_far:
                max_so_far = sum_so_far
            sum_so_far = 0

    common.part(1, max_so_far)

    blocks = []
    sum_so_far = 0
    for line in text.split("\n"):
        if line != "":
            sum_so_far += int(line)
        else:
            blocks.append(sum_so_far)
            sum_so_far = 0

    common.part(2, sum(sorted(blocks)[-3:]))
