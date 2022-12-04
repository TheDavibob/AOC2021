import numpy as np
import common


def overlap(range_strings):
    range_0, range_1 = range_strings.split(",")
    points_0 = [int(n) for n in range_0.split("-")]
    points_1 = [int(n) for n in range_1.split("-")]

    if (points_0[0] <= points_1[0]) and (points_0[1] >= points_1[1]):
        return True
    elif (points_1[0] <= points_0[0]) and (points_1[1] >= points_0[1]):
        return True
    else:
        return False


def overlap_2(range_strings):
    range_0, range_1 = range_strings.split(",")
    points_0 = [int(n) for n in range_0.split("-")]
    points_1 = [int(n) for n in range_1.split("-")]

    all_0 = [n for n in range(points_0[0], points_0[1]+1)]
    all_1 = [n for n in range(points_1[0], points_1[1]+1)]

    if set(all_0).intersection(set(all_1)):
        return True
    else:
        return False


if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    overlaps = 0
    for line in text.split("\n"):
        if line == "":
            continue

        overlaps += overlap(line)

    common.part(1, overlaps)

    overlaps = 0
    for line in text.split("\n"):
        if line == "":
            continue

        overlaps += overlap_2(line)

    common.part(2, overlaps)
