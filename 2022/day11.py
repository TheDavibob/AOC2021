import math
from copy import copy

import numpy as np
from tqdm import tqdm

import common


class Monkey:
    def __init__(self, block_text):
        lines = block_text.split("\n")
        self.number = int(lines[0][-2])
        worry_levels = lines[1].split(": ")[1]
        self.worry_levels = [int(worry_level) for worry_level in worry_levels.split(", ")]
        operation = lines[2].split(": ")[1].split(" = ")[-1]

        def fun(old):
            new = eval(operation)
            return new

        self.operation = fun

        test = lines[3].split(": ")[1]
        self.test_divisor = int(test.split(" ")[-1])

        self.if_true = int(lines[4].split(" ")[-1])
        self.if_false = int(lines[5].split(" ")[-1])

        self.inspection_count = 0


def step(monkeys: list[Monkey], n_worry, lcm = None, debug=False):
    for monkey in monkeys:
        while monkey.worry_levels:
            monkey.inspection_count += 1
            worry_level = monkey.worry_levels.pop(0)
            new_worry_level = monkey.operation(worry_level)
            new_worry_level = new_worry_level // n_worry

            if lcm:
                new_worry_level = new_worry_level % lcm

            if new_worry_level % monkey.test_divisor == 0:
                new_monkey = monkey.if_true
            else:
                new_monkey = monkey.if_false

            target = [m for m in monkeys if m.number == new_monkey][0]
            target.worry_levels.append(new_worry_level)
            if debug:
                print(f"Item with worry level {new_worry_level} thrown to monkey {new_monkey}")

    return monkeys


def step_single_item(worry_level, monkey, monkeys: list[Monkey], monkey_count, n_worry, lcm):
    old_monkey = 0
    while monkey >= old_monkey:
        monkey_count[monkey] += 1
        old_monkey = monkey
        worry_level = monkeys[monkey].operation(worry_level)
        worry_level = worry_level // n_worry

        worry_level %= lcm

        if worry_level % monkeys[monkey].test_divisor == 0:
            monkey = monkeys[monkey].if_true
        else:
            monkey = monkeys[monkey].if_false

    return worry_level, monkey, monkey_count


test_input = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    # print(text)

    # text = test_input

    monkeys = []
    for block in text.split("\n\n"):
        monkeys.append(Monkey(block))

    n_worry = 3
    for round in range(20):
        monkeys = step(monkeys, n_worry)

    inspection_counts = [m.inspection_count for m in monkeys]

    common.part(1, math.prod(sorted(inspection_counts)[-2:]))

    monkeys = []
    for block in text.split("\n\n"):
        monkeys.append(Monkey(block))

    monkeys = []
    for block in text.split("\n\n"):
        monkeys.append(Monkey(block))

    n_worry = 1
    lcm = math.lcm(*[monkey.test_divisor for monkey in monkeys])
    for round in range(10000):
        monkeys = step(monkeys, n_worry, lcm)

    monkey_counts = [m.inspection_count for m in monkeys]

    common.part(2, math.prod(sorted(monkey_counts)[-2:]))
