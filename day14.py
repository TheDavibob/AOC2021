from copy import copy

import numpy as np
import common


def parse_input(text):
    initial, instructions = text.split('\n\n')

    locations = {}
    for line in instructions.split('\n'):
        if line != "":
            a, b = line.split(' -> ')
            locations[a] = b

    return initial, locations


def iterate(before, counts, insertion_mapping):
    after = [x for x in before]
    loc = 0
    for a, b in zip(before[:-1], before[1:]):
        loc += 1
        if a + b in insertion_mapping.keys():
            new_char = insertion_mapping[a + b]
            after.insert(loc, new_char)
            counts[new_char] = counts.get(new_char, 0) + 1
            loc += 1

    return "".join(after), counts


def get_counts(string):
    counts = {}
    for char in set(string):
        counts[char] = string.count(char)

    return counts


def trim_string(new_string, old_string):
    start_idx = 0
    for i in range(len(new_string)):
        if new_string[:i] != old_string[:i]:
            start_idx = i-1
            break

    end_idx = len(new_string)
    for i in range(len(new_string)):
        if new_string[-(i+1):] != old_string[-(i+1)]:
            end_idx = -i
            break

    return new_string[start_idx:end_idx]


def count_after(pair, num, insertion_mapping):
    # have pair of letters 'XY'
    count = {}
    if num == 0:
        return count

    if pair in insertion_mapping.keys():
        count = {insertion_mapping[pair] : 1}
        pair_0_count = count_after(pair[0] + insertion_mapping[pair], num-1, insertion_mapping)
        pair_1_count = count_after(insertion_mapping[pair] + pair[1], num-1, insertion_mapping)
        for k, v in pair_0_count.items():
            count[k] = count.get(k, 0) + v

        for k, v in pair_1_count.items():
            count[k] = count.get(k, 0) + v

    return count


def iterate_over_pairs(pairs_count, insertion_mapping):
    new_pairs_count = {}
    for pair in pairs_count.keys():
        num_occurances = pairs_count[pair]
        if pair in insertion_mapping.keys():
            new_char = insertion_mapping[pair]
            new_pairs_count[pair[0] + new_char] = new_pairs_count.get(pair[0] + new_char, 0) + num_occurances
            new_pairs_count[new_char + pair[1]] = new_pairs_count.get(new_char + pair[1], 0) + num_occurances
        else:
            new_pairs_count[pair] = new_pairs_count.get(pair, 0) + num_occurances

    return new_pairs_count


if __name__ == "__main__":
    text = common.import_file("input/day14_input")
    initial, location = parse_input(text)

    string = copy(initial)
    counts = get_counts(string)
    for _ in range(10):
        new_string, counts = iterate(string, counts, location)
        # string = trim_string(new_string, string)
        string = new_string

    print(max(counts.values()) - min(counts.values()))

    counts = get_counts(initial)
    for pair_0, pair_1 in zip(initial[:-1], initial[1:]):
        new_counts = count_after(pair_0 + pair_1, 10, location)
        for k, v in new_counts.items():
            counts[k] = counts.get(k, 0) + v

    print(max(counts.values()) - min(counts.values()))

    pairs = []
    for pair_0, pair_1 in zip(initial[:-1], initial[1:]):
        pairs.append(pair_0 + pair_1)

    pairs_count = {pair: initial.count(pair) for pair in pairs}
    for _ in range(40):
        pairs_count = iterate_over_pairs(pairs_count, location)

    char_count = {}
    for k, v in pairs_count.items():
        char_count[k[0]] = char_count.get(k[0], 0) + v
        char_count[k[1]] = char_count.get(k[1], 0) + v

    char_count[initial[0]] = char_count[initial[0]] + 1
    char_count[initial[-1]] = char_count[initial[-1]] + 1

    print((max(char_count.values()) - min(char_count.values())) // 2)