TEST_DATA = """987654321111111
811111111111119
234234234234278
818181911112111"""

with open("data/day_03") as f:
    REAL_DATA = f.read()


def max_joltage(num_str):
    loc=None
    for n in range(10):
        this_n = str(9 - n)
        if this_n in num_str[:-1]:
            leading_num = this_n
            loc = num_str.index(this_n)
            break

    for n in range(9):
        this_n = str(9 - n)
        if this_n in num_str[loc+1:]:
            trailing_num = this_n
            break

    return int(leading_num + trailing_num)


def part_one(input, debug=False):
    total_joltage = 0
    for line in input.split("\n"):
        new_joltage = max_joltage(line)
        total_joltage += new_joltage

        if debug:
            print(line, new_joltage)

    return total_joltage


def max_joltage_iterative(num_str, n_digits):
    all_digits = ""
    loc = -1
    for this_digit in range(n_digits):
        to_exclude = n_digits - this_digit - 1
        if to_exclude > 0:
            reduced_str = num_str[loc+1:-to_exclude]
        else:
            reduced_str = num_str[loc+1:]

        found = False
        for n in range(10):
            this_n = str(9 - n)
            if this_n in reduced_str:
                leading_num = this_n
                loc = num_str[loc+1:].index(this_n) + loc + 1
                found = True
                break
        all_digits += leading_num

    return int(all_digits)


def part_two(input, n_digits=12, debug=False):
    total_joltage = 0
    for line in input.split("\n"):
        new_joltage = max_joltage_iterative(line, n_digits)
        total_joltage += new_joltage

        if debug:
            print(line, new_joltage)

    return total_joltage


if __name__ == "__main__":
    assert part_one(TEST_DATA, debug=False) == 357


    print("Part 1:", part_one(REAL_DATA))

    assert part_two(TEST_DATA, n_digits=2, debug=False) == 357
    assert part_two(TEST_DATA, n_digits=12, debug=False) == 3121910778619

    print("Part 2:", part_two(REAL_DATA))