from copy import copy

import numpy as np

import common


def parse_input(text):
    numbers = []
    for line in text.split("\n"):
        if line == "":
            continue

        numbers.append(int(line))

    return numbers


def sort_list(numbers: list[int], verbose=False):
    original_list = copy(numbers)
    for number in original_list:
        current_index = numbers.index(number)
        number = numbers.pop(current_index)
        new_index = (current_index + number)
        new_index %= len(numbers)
        numbers.insert(new_index, number)
        if verbose:
            print(f"Moving {number} from {current_index} to {new_index}")
            # print(numbers)

    return numbers


def slow_move(numbers, number_to_move):
    print(numbers)
    if number_to_move > 0:
        for _ in range(number_to_move):
            current_index = numbers.index(number_to_move)
            numbers.pop(current_index)
            numbers.insert((current_index + 1) % len(numbers), number_to_move)
            print(numbers)

    else:
        for _ in range(-number_to_move):
            current_index = numbers.index(number_to_move)
            numbers.pop(current_index)
            numbers.insert((current_index - 1) % len(numbers), number_to_move)
            print(numbers)

    return numbers



class CircularList:
    def __init__(self, numbers):
        self.map = {}
        for fro, to in zip(numbers[:-1], numbers[1:]):
            self.map[fro] = to

        self.map[numbers[-1]] = numbers[0]

    def move(self, number):
        ...


test_input = """1
2
-3
3
-2
0
4"""

if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    numbers = parse_input(text)

    sorted_list = sort_list(numbers, verbose=True)

    zero_index = sorted_list.index(0)
    coordinates = [
        sorted_list[(zero_index + n) % len(numbers)]
        for n in (1000, 2000, 3000)
    ]
    common.part(1, sum(coordinates))

    common.part(2, "TBC")
