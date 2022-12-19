import numpy as np
import common


def parse_input(text):
    voxels = []
    for line in text.split("\n"):
        if line == "":
            continue

        point = tuple(int(x) for x in line.split(","))
        voxels.append(point)
    return voxels


def adj_count(voxel, voxels):
    adj_sides = 0
    for delta in range(3):
        for sign in (-1, 1):
            change = [0, 0, 0]
            change[delta] = sign

            scan_point = tuple(
                v + j for v, j in zip(voxel, change)
            )

            if scan_point in voxels:
                adj_sides += 1

    return adj_sides


def free_sides(voxels):
    free = 0
    for voxel in voxels:
        free += 6 - adj_count(voxel, voxels)

    return free


def find_outside(voxels):
    mins = [min([v[i] for v in voxels]) for i in range(3)]
    maxs = [max([v[i] for v in voxels]) for i in range(3)]
    cube = min(mins) - 1, max(maxs) + 1

    outside = []
    outside.append((cube[0], cube[0], cube[0]))
    changed = True
    while changed:
        changed = False
        for point in outside:
            for delta in range(3):
                for sign in (-1, 1):
                    change = [0, 0, 0]
                    change[delta] = sign

                    scan_point = tuple(
                        v + j for v, j in zip(point, change)
                    )

                    if min(scan_point) < cube[0]:
                        continue
                    if max(scan_point) > cube[1]:
                        continue

                    if scan_point in outside:
                        continue

                    if scan_point not in voxels:
                        outside.append(scan_point)
                        changed = True

    return outside


def outside_count(voxels, outside):
    exterior_sides = 0
    for voxel in voxels:
        for delta in range(3):
            for sign in (-1, 1):
                change = [0, 0, 0]
                change[delta] = sign

                scan_point = tuple(
                    v + j for v, j in zip(voxel, change)
                )

                if scan_point in outside:
                    exterior_sides += 1

    return exterior_sides

test_text = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    voxels = parse_input(text)

    # voxels = [(1, 1, 1), (2, 1, 1)]

    common.part(1, free_sides(voxels))

    outside = find_outside(voxels)
    common.part(2, outside_count(voxels, outside))
