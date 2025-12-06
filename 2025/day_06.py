# /// script
# dependencies = [
# ]
# ///
from math import prod

TEST_DATA = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """


with open("data/day_06") as f:
    REAL_DATA = f.read()


def parse_puzzle_input(puzzle_input):
    data_lines = []

    for line in puzzle_input.split("\n"):
        data = []
        is_op = False
        for bit in line.split(" "):
            if bit in ["", " "]: continue

            if bit in ["*", "+"]:
                is_op = True
                data.append(bit)

            else:
                data.append(int(bit))

        if is_op:
            op_line = data
        else:
            data_lines.append(data)

    return data_lines, op_line


def part_one(puzzle_input):
    data_lines, op_line = parse_puzzle_input(puzzle_input)

    total = 0
    for i, op in enumerate(op_line):
        numbers = [d[i] for d in data_lines]
        if op == "*":
            total += prod(numbers)
        elif op == "+":
            total += sum(numbers)
        else:
            raise ValueError(f"Op {op} not understood")

    return total


def parse_input_again(puzzle_input):
    op_line = puzzle_input.split("\n")[-1]

    ops = []
    op_index = []
    for i_symbol, symbol in enumerate(op_line):
        if symbol not in [" ", "."]:
            ops.append(symbol)
            op_index.append(i_symbol)

    op_index.append(len(op_line))
    total = 0
    for from_index, to_index, op in zip(op_index[:-1], op_index[1:], ops):
        numbers = []
        for index in range(from_index, to_index):
            number = ""
            for data_line in puzzle_input.split("\n")[:-1]:
                char = data_line[index]
                if char != " ":
                    number += char

            if number != "":
                numbers.append(int(number))

        print(numbers, op)

        if op == "*":
            total += prod(numbers)
        else:
            total += sum(numbers)

    return total


if __name__ == "__main__":
    # assert part_one(TEST_DATA) == 4277556
    # print(f"Part 1: {part_one(REAL_DATA)}")

    # assert parse_input_again(TEST_DATA) == 3262769
    # 11708563457309 is too low...
    # 11708563457820 is also too low...
    print(f"Part 2: {parse_input_again(REAL_DATA)}")