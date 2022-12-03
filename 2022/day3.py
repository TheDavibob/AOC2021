import numpy as np
import common


def line_to_vals(line):
    vals = []
    for character in line:
        val = ord(character)
        if val >= 97:
            val = val - 96
        else:
            val = val - 38
        vals.append(val)

    return vals


def vals_to_common(vals):
    part_1 = vals[:len(vals)//2]
    part_2 = vals[len(vals)//2:]

    common_parts = set(part_1) & set(part_2)

    return list(common_parts)[0]


def three_lines_to_common(lines):
    vals = []
    for line in lines:
        vals.append(line_to_vals(line))

    common_parts = set(vals[0]) & set(vals[1]) & set(vals[2])

    return list(common_parts)[0]


if __name__ == "__main__":
    text = common.import_file("input/day3")

    common_sum = 0
    for line in text.split("\n"):
        if line == "":
            continue

        vals = line_to_vals(line)
        common_value = vals_to_common(vals)
        common_sum += common_value

    common.part(1, common_sum)

    common_sum = 0
    lines = [l for l in text.split("\n") if l != ""]
    for i in range(len(lines) // 3):
        common_sum += three_lines_to_common(lines[3*i:3*i+3])

    common.part(2, common_sum)
