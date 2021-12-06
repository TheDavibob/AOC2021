import numpy as np

import common


def get_intersections(starts, ends, part_two=False):
    mask = np.zeros((1000, 1000), dtype=int)
    for s, e in zip(starts, ends):
        if s[0] == e[0]:
            start = s[1]
            end = e[1]

            if end > start:
                for i in range(end - start + 1):
                    mask[s[0], s[1] + i] += 1
            else:
                for i in range(start - end + 1):
                    mask[s[0], e[1] + i] += 1
        elif s[1] == e[1]:
            start = s[0]
            end = e[0]
            if end > start:
                for i in range(end - start + 1):
                    mask[s[0] + i, s[1]] += 1
            else:
                for i in range(start - end + 1):
                    mask[e[0] + i, s[1]] += 1
        else:
            if part_two:
                if e[0] > s[0]:
                    x_dir = 1
                else:
                    x_dir = -1

                if e[1] > s[1]:
                    y_dir = 1
                else:
                    y_dir = -1

                for i in range(abs(e[0] - s[0]) + 1):
                    mask[s[0] + x_dir * i, s[1] + y_dir * i] += 1

    return np.sum(mask > 1)


if __name__ == "__main__":
    text = common.import_file('input/day5_input')

    starts = []
    ends = []
    for line in text.split('\n'):
        if line != '':
            start, end = line.split(' -> ')
            s_x, s_y = [int(s) for s in start.split(',')]
            e_x, e_y = [int(s) for s in end.split(',')]

            starts.append((s_x, s_y))
            ends.append((e_x, e_y))

    starts = np.array(starts)
    ends = np.array(ends)

    print(f"Part 1: {get_intersections(starts, ends)}")
    print(f"Part 2: {get_intersections(starts, ends, part_two=True)}")