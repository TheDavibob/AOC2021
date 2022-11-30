import operator
from itertools import permutations

import common


def parse_input(text):
    distance_dict = {}
    for line in text.split('\n'):
        if line == "":
            continue

        start, _, end, _, dist = line.split(' ')
        distance_dict[(start, end)] = int(dist)
        distance_dict[(end, start)] = int(dist)
    return distance_dict


def brute_force_travelling_salesman(distance_dict, method):
    nodes = {k[0] for k in distance_dict.keys()}
    if method == "minimise":
        best_distance = max(v for v in distance_dict.values()) * len(nodes)
        minimise = True
        method = operator.lt

    elif method == "maximise":
        best_distance = 0
        minimise = False
        method = operator.gt
    else:
        ValueError("Method must be one of 'minimise', 'maximise'")

    best_permutation = None
    for p in permutations(nodes):
        distance = 0
        for start, end in zip(p[:-1], p[1:]):
            distance += distance_dict[(start, end)]
            if minimise and distance > best_distance:
                break

        if method(distance, best_distance):
            best_distance = distance
            best_permutation = p

    return best_distance, best_permutation



if __name__ == "__main__":
    text = common.load_input(9)
    distance_dict = parse_input(text)
    shortest_distance, best_permutation = brute_force_travelling_salesman(distance_dict, method='minimise')
    common.part(1, shortest_distance)
    largest_distance, best_permutation = brute_force_travelling_salesman(distance_dict, method='maximise')
    common.part(1, largest_distance)