import numpy as np

import intcode
import common


class TractorTestor:
    def __init__(self, code):
        self.code = code

    def test_point(self, x, y):
        s = intcode.Intcode(self.code)
        s.input_list = [x, y]
        s.step_all()
        return s.output_list[0]

    def test_all_points(self):
        pulled = 0
        for x in range(50):
            for y in range(50):
                is_pulled = self.test_point(x, y)
                pulled += is_pulled

        return pulled

    def test_on_grid(self, x_max, y_max):
        grid = np.zeros((y_max, x_max), dtype=bool)
        for x in range(x_max):
            for y in range(y_max):
                grid[y, x] = self.test_point(x, y)

        return grid

    def find_height_equal_target(self, target, initial_x=4):
        # Finding where the height of the ray is equal to something
        x = initial_x
        top_y = 0
        while True:
            y = top_y
            found_top = False
            while not found_top:
                found_top = bool(self.test_point(x, y))
                if found_top:
                    top_y = y
                y+=1

            this_column_count = 1
            found_bottom = False
            while not found_bottom:
                found_bottom = not bool(self.test_point(x, y))
                if not found_bottom:
                    this_column_count += 1
                y+=1

            if this_column_count >= target:
                break
            else:
                x += 1

        return y

    def find_next_top_edge(self, prev_top_edge):
        x = prev_top_edge[0]
        y = prev_top_edge[1]

        x += 1
        y += 1
        while True:
            inside = self.test_point(x, y)
            if not inside:
                return (x-1, y)
            else:
                x += 1

    def find_next_bottom_edge(self, prev_top_edge):
        x = prev_top_edge[0]
        y = prev_top_edge[1]

        y += 1
        x += 1
        while True:
            inside = self.test_point(x, y)
            if not inside:
                return (x, y-1)
            else:
                y += 1

    def trace_edges(self, reps=10):
        initial_point = (4, 3)
        top_edges = [initial_point]
        bottom_edges = [initial_point]
        for _ in range(reps):
            top_edges.append(self.find_next_top_edge(top_edges[-1]))
            bottom_edges.append(self.find_next_bottom_edge(bottom_edges[-1]))

        return top_edges, bottom_edges


def find_100_square(s):
    upper, lower = s.trace_edges(2000)
    for u in upper:
        for l in lower:
            if (u[0] - l[0] == 99) and (l[1] - u[1] == 99):
                potential = (u, l)
                break

    upper_corner = (potential[1][0], potential[0][1])
    return upper_corner


if __name__ == "__main__":
    code = common.import_file("../input/day19")
    s = TractorTestor(code)
    common.part(1, s.test_all_points())
    upper_corner = find_100_square(s)
    common.part(2, upper_corner[0]*10000 + upper_corner[1])