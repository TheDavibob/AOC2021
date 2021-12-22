import numpy as np
from copy import copy

import common

def parse_input(text):
    state = []
    xyz = []
    for line in text.split('\n'):
        if line == "":
            continue

        onoff, coords = line.split(' ')
        x, y, z = coords.split(',')
        xmin, xmax = [int(s) for s in x.split('=')[-1].split('..')]
        ymin, ymax = [int(s) for s in y.split('=')[-1].split('..')]
        zmin, zmax = [int(s) for s in z.split('=')[-1].split('..')]

        if onoff == "on":
            state.append(1)
        else:
            state.append(0)

        xyz.append([(xmin, xmax), (ymin, ymax), (zmin, zmax)])

    return state, xyz


def part_1(state, xyz):
    initial_input = np.zeros((101, 101, 101), dtype=bool)
    for state, coords in zip(state, xyz):
        initial_input[
            coords[0][0]+50:coords[0][1]+51,
            coords[1][0]+50:coords[1][1]+51,
            coords[2][0]+50:coords[2][1]+51,
        ] = state

    return np.sum(initial_input)



def get_overlap(coord0, coord1):
    overlap_region = []
    is_overlap = True
    for c0, c1 in zip(coord0, coord1):
        axis_overlap = ((max(c0[0], c1[0])), (min(c0[1], c1[1])))
        if axis_overlap[0] > axis_overlap[1]:
            is_overlap = False
        overlap_region.append(axis_overlap)

    if is_overlap:
        return overlap_region
    else:
        return None


def inclusion_exclusion(include, exclude, new_coord, state):
    new_include = copy(include)
    new_exclude = copy(exclude)

    if state:
        new_include.append(new_coord)

    # The inclusion/exclusion algebra is independent of state, except for
    # the inclusion above
    for i in include:
        overlap = get_overlap(i, new_coord)
        if overlap:
            new_exclude.append(overlap)

    for e in exclude:
        overlap = get_overlap(e, new_coord)
        if overlap:
            new_include.append(overlap)

    return new_include, new_exclude


def inc_exc_loop(state, xyz):
    include, exclude = [], []
    for i, (s, c) in enumerate(zip(state, xyz)):
        include, exclude = inclusion_exclusion(include, exclude, c, s)
        if i % 10 == 0:
            print(f"Progress: {100*i/len(state):0.2f}%%")

    sum = 0
    for c in include:
        size = (c[0][1]+1 - c[0][0])*(c[1][1]+1 - c[1][0])*(c[2][1]+1 - c[2][0])
        sum += size

    for c in exclude:
        size = (c[0][1]+1 - c[0][0])*(c[1][1]+1 - c[1][0])*(c[2][1]+1 - c[2][0])
        sum -= size

    return sum


if __name__ == "__main__":
    print("Testing algorithm")
    test_text = common.import_file('input/day22_test2')
    state, xyz = parse_input(test_text)
    assert part_1(state, xyz) == 474140
    assert inc_exc_loop(state, xyz) == 2758514936282235
    print("Test passed")

    text = common.import_file('input/day22_input')
    state, xyz = parse_input(text)
    print(f"Part 1: {part_1(state, xyz)}")
    print(f"Part 2: {inc_exc_loop(state, xyz)}")
