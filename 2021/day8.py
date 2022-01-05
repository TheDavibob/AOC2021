import numpy as np
import common

map = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg'
}


def decode_line(line):
    test_values, evaluation_values = line.split(' | ')
    segments = test_values.split(' ')

    mapping_int_to_str = dict()

    # Write in the "easy" ones
    for i, s in enumerate(segments):
        if len(s) == 2:
            mapping_int_to_str[1] = s
        elif len(s) == 4:
            mapping_int_to_str[4] = s
        elif len(s) == 3:
            mapping_int_to_str[7] = s
        elif len(s) == 7:
            mapping_int_to_str[8] = s


    # Lets do some logic on the ones of lengths 6
    sixes = [s for s in segments if len(s) == 6]
    for s in sixes:
        # 0 and 9 both overlap completely with 1, 6 does not
        for c in mapping_int_to_str[1]:
            if c not in s:
                mapping_int_to_str[6] = s
                break

    for s in sixes:
        # 9 overlaps completely with 4, 0 does not
        if s != mapping_int_to_str[6]:
            for c in mapping_int_to_str[4]:
                if c not in s:
                    mapping_int_to_str[0] = s
                    break

    for s in sixes:
        # Only 9 remains
        if s not in [mapping_int_to_str[0], mapping_int_to_str[6]]:
            mapping_int_to_str[9] = s

    fives = [s for s in segments if len(s) == 5]
    for s in fives:
        # 3 overlaps completely with 1
        if all([c in s for c in mapping_int_to_str[1]]):
            mapping_int_to_str[3] = s
            break

    for s in fives:
        # 5 is completely contained within 6
        if s != mapping_int_to_str[3]:
            for c in s:
                if c not in mapping_int_to_str[6]:
                    mapping_int_to_str[2] = s
                    break

    for s in fives:
        if s not in [mapping_int_to_str[3], mapping_int_to_str[2]]:
            mapping_int_to_str[5] = s

    # Flip the mapping, sorting the keys alphabetically
    mapping_char_to_int = {''.join(sorted(v)): k for k, v in mapping_int_to_str.items()}

    # Create the output
    out_str = ''
    for char in evaluation_values.split(' '):
        # Sort the output char, so will match the keys
        alpha_char = ''.join(sorted(char))
        out_str += str(mapping_char_to_int[alpha_char])

    return int(out_str)


if __name__ == "__main__":
    text = common.import_file('input/day8_input')

    # Part 1
    count = 0
    for line in text.split('\n'):
        if line != "":
            chopped = line.split(('|'))
            segments = chopped[-1].split(' ')
            for s in segments:
                if len(s) in [2, 3, 4, 7]:
                    count += 1

    print(f"Part 1: {count}")

    # Part 2
    total = 0
    for line in text.split('\n'):
        if line != "":
            total += decode_line(line)

    print(f"Part 2: {total}")
