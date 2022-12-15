import numpy as np
from tqdm import tqdm

import common


def parse_input(text):
    points = []

    for line in text.split("\n"):
        if line == "":
            continue

        sensor, beacon = line.split(": ")

        s_xy = sensor.split(" at ")[-1]
        s_x, s_y = s_xy.split(", ")
        s_x = int(s_x.split("=")[-1])
        s_y = int(s_y.split("=")[-1])

        b_xy = beacon.split(" at ")[-1]
        b_x, b_y = b_xy.split(", ")
        b_x = int(b_x.split("=")[-1])
        b_y = int(b_y.split("=")[-1])

        points.append({"sensor": (s_x, s_y), "beacon": (b_x, b_y)})

    return points


def how_many_blocked(points, line_no):
    for p in points:
        p["distance"] = (
            abs(p["sensor"][0] - p["beacon"][0])
            + abs(p["sensor"][1] - p["beacon"][1])
        )

    # min_y = min(
    #     min([a["beacon"][1] for a in points]),
    #     min([a["sensor"][1] - a["distance"] for a in points])
    # )
    # max_y = max(
    #     max([a["beacon"][1] for a in points]),
    #     max([a["sensor"][1] + a["distance"] for a in points])
    # )
    #
    # print(min_y, max_y)

    y = line_no
    bit_blocked = []
    for point in points:
        sensor = point["sensor"]
        distance = point["distance"]
        y_dist = abs(sensor[1] - y)
        if y_dist > distance:
            continue

        rem_dist = distance - y_dist
        bit_blocked.append((sensor[0]-rem_dist, sensor[0]+rem_dist))

    bit_blocked = sorted(bit_blocked, key=lambda x: x[1] - x[0])[::-1]

    # Hack: they overlap
    delta = max(b[1] for b in bit_blocked) - min(b[0] for b in bit_blocked) + 1

    beacons = set(point["beacon"] for point in points)
    beacons_on_line = len([beacon for beacon in list(beacons) if beacon[1] == line_no])

    sensors = set(point["sensor"] for point in points)
    sensors_on_line = len([sensor for sensor in list(sensors) if sensor[1] == line_no])

    return delta-beacons_on_line-sensors_on_line, bit_blocked


def reduce_to_interval(a, b):
    if (a[1] < b[0]) or (b[1] < a[0]):
        return [a, b]

    min_val = min(a[0], b[0])
    max_val = max(a[1], b[1])
    return [(min_val, max_val)]


def reduce_bit_blocked(bit_blocked):
    is_reduced=True
    while is_reduced:
        is_reduced = False
        for i, b in enumerate(bit_blocked):
            for j, c in enumerate(bit_blocked[:i] + bit_blocked[i+1:]):
                out = reduce_to_interval(b, c)
                if len(out) == 1:
                    bit_blocked.remove(b)
                    bit_blocked.remove(c)
                    bit_blocked.append(out[0])
                    is_reduced = True
                    break
            if is_reduced:
                break

    return bit_blocked

demo_text="""
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""


if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    # text = demo_text

    points = parse_input(text)
    n_blocked, bit_blocked = how_many_blocked(points, 2000000)
    bit_blocked = reduce_bit_blocked(bit_blocked)

    common.part(1, n_blocked)

    for line in tqdm(range(4000000)):
        n_blocked, bit_blocked = how_many_blocked(points, line)
        bit_blocked = reduce_bit_blocked(bit_blocked)
        if len(bit_blocked) == 2:
            break

    edge = max(bit_blocked[0][0], bit_blocked[1][0])
    missing_point = edge-1

    common.part(2, missing_point * 4000000 + line)
