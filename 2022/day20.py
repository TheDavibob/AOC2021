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


def sort_list(numbers: list[int], original_list, index_array, verbose=False):
    for index, number in enumerate(original_list):
        # current_index = numbers.index(number)
        current_index = index_array[index]

        number = numbers.pop(current_index)
        new_index = (current_index + number)
        new_index %= len(numbers)

        if new_index < current_index:
            index_array[(index_array >= new_index) & (index_array <= current_index)] += 1
        elif new_index > current_index:
            index_array[(index_array <= new_index) & (index_array >= current_index)] -= 1
        index_array[index] = new_index

        numbers.insert(new_index, number)
        if verbose:
            print(f"Moving {number} from {current_index} to {new_index}")
            print(numbers)
            print(index_array)

    return numbers, index_array


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
    numbers = parse_input(test_input)
    original_list = copy(numbers)
    index_array = np.arange(len(original_list), dtype=int)

    sorted_list, _ = sort_list(numbers, original_list, index_array, verbose=False)

    zero_index = sorted_list.index(0)
    coordinates = [
        sorted_list[(zero_index + n) % len(numbers)]
        for n in (1000, 2000, 3000)
    ]
    common.part(1, sum(coordinates))

    new_list = [x * 811589153 for x in original_list]
    new_original = copy(new_list)
    index_array = np.arange(len(new_original), dtype=int)
    for _ in range(10):
        new_list, index_array = sort_list(new_list, new_original, index_array, verbose=False)

    zero_index = new_list.index(0)
    coordinates = [
        new_list[(zero_index + n) % len(numbers)]
        for n in (1000, 2000, 3000)
    ]

    common.part(2, sum(coordinates))
