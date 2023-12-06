import math

import common

def parse_input(text):
    times, distance = text.split("\n")
    time = times.split(":")[-1]
    dist = distance.split(":")[-1]
    all_times = [int(x) for x in time.split(" ") if x != ""]
    all_dists = [int(x) for x in dist.split(" ") if x != ""]

    dist_to_time_map = {}
    for t, d in zip(all_times, all_dists):
        dist_to_time_map[d] = t

    return dist_to_time_map


def part_one(parsed_input, no=1):
    n_wins = []
    for d, t in parsed_input.items():
        threshold_lower = (t - math.sqrt(t**2 - 4*d)) / 2
        threshold_upper = (t + math.sqrt(t**2 - 4*d)) / 2

        n_wins.append(math.floor(threshold_upper) - math.ceil(threshold_lower) + 1)

    common.part(no, math.prod(n_wins))


def part_two(parsed_input):
    all_d = ""
    all_t = ""
    for d, t in parsed_input.items():
        all_d = all_d + str(d)
        all_t = all_t + str(t)

    new_input = {int(all_d): int(all_t)}
    part_one(new_input, no=2)


if __name__ == "__main__":
    text = common.import_file("input/day6")
    parsed_input = parse_input(text)
    part_one(parsed_input)
    part_two(parsed_input)
