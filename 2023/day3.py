import common


def parse_input(input):
    lines = input.split("\n")

    number_blocks = []
    chars = []
    for i_line, line in enumerate(lines):
        if line == "":
            continue

        is_number = False
        start_digit = 0
        end_digit = 0
        for i_char, char in enumerate(line):
            if is_number and (not char.isnumeric()):
                end_digit = i_char
                number_blocks.append((int(line[start_digit:end_digit]), i_line, (start_digit, end_digit-1)))
                is_number = False

                if char != ".":
                    chars.append((char, i_line, i_char))

            elif not is_number and char.isnumeric():
                start_digit = i_char
                is_number = True

            elif not is_number and char != ".":
                chars.append((char, i_line, i_char))

        if is_number:  # end of line:
            end_digit = len(line)
            number_blocks.append((int(line[start_digit:end_digit]), i_line, (start_digit, end_digit-1)))

    return number_blocks, chars


def part_one(text):
    digits, chars = parse_input(text)
    valid_nos = []
    for seq, line, (start, stop) in digits:
        for other_seq, other_line, loc in chars:
            if (other_seq == seq) and (other_line == line) and (loc == start):
                continue

            if other_line == line:
                if (loc == start-1) or (loc == stop+1):
                    valid_nos.append(int(seq))
                    break
            elif (other_line == line+1) or (other_line == line-1):
                if (loc >= start-1) and (loc <= stop+1):
                    valid_nos.append(int(seq))
                    break

    print(valid_nos)

    common.part(1, sum(valid_nos))


def part_two(text):
    digits, chars = parse_input(text)
    gear_ratios = []
    for char, line, loc in chars:
        if char != "*":
            continue

        adj_digits = []
        for digit, digit_line, (start, stop) in digits:
            if digit_line not in (line-1, line, line+1):
                continue

            if loc >= start-1 and loc <= stop+1:
                adj_digits.append(digit)

        if len(adj_digits) == 2:
            gear_ratios.append(adj_digits[0] * adj_digits[1])

    print(gear_ratios)
    common.part(2, sum(gear_ratios))


if __name__ == "__main__":
    text = common.import_file("input/day3")
    part_one(text)
    part_two(text)
