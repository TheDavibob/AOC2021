import math

import common

def parse_input(text):
    lines = text.split("\n")
    sequences = []
    for line in lines:
        if line == "":
            continue

        sequences.append([int(x) for x in line.split()])

    return sequences


def diff(sequence):
    return [x-y for x, y in zip(sequence[1:], sequence[:-1])]


def polyfit(sequence):
    layers = []
    layers.append(sequence)
    while any(layers[-1]):
        layers.append(diff(layers[-1]))

    flipped_layers = layers[::-1]
    flipped_layers[0].append(0)
    for i_layer, layer in enumerate(flipped_layers[1:]):
        layer.append(layer[-1] + flipped_layers[i_layer][-1])

    return layers[0][-1]


def part_one(sequences):
    sum = 0
    for sequence in sequences:
        sum += polyfit(sequence)

    common.part(1, sum)


def part_two(sequences):
    sum = 0
    for sequence in sequences:
        sum += polyfit(sequence[::-1])

    common.part(2, sum)


if __name__ == "__main__":
    text = common.import_file("input/day9")
    sequences = parse_input(text)

    part_one(sequences)
    part_two(sequences)