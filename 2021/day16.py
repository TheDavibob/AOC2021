from math import prod

import numpy as np

import common

def decompose_binary_string(string, len_output=None):
    current_position = 0
    output = []
    version_sum = 0
    while current_position < len(string):
        if len_output and (len(output) >= len_output):
            break

        if "1" not in string[current_position:]:
            break

        version = string[current_position:current_position+3]
        typeID = string[current_position+3:current_position+6]
        current_position += 6
        if int(typeID, 2) == 4:
            number = ""
            while True:
                number = number + string[current_position+1:current_position+5]
                if string[current_position] == "1":
                    current_position = current_position + 5
                else:
                    current_position = current_position + 5
                    break
            output.append((int(version, 2), int(typeID, 2), int(number, 2)))
            version_sum += int(version, 2)
        else:
            length_type_id = int(string[current_position])
            current_position += 1
            if length_type_id:
                length = 11
                num_subpackets = int(string[current_position:current_position + length], 2)
                current_position += length
                new_output, new_position, new_version_sum = decompose_binary_string(string[current_position:], num_subpackets)
                output.append((int(version, 2), int(typeID, 2), new_output))
                version_sum += new_version_sum + int(version, 2)
                current_position += new_position
            else:
                length = 15
                len_subpackets = int(string[current_position:current_position + length], 2)
                current_position += length
                subpacket_string = string[current_position:current_position+len_subpackets]
                new_output, new_position, new_version_sum = decompose_binary_string(subpacket_string)
                output.append((int(version, 2), int(typeID, 2), new_output))
                version_sum += new_version_sum + int(version, 2)
                current_position += new_position

    return output, current_position, version_sum


def decompose_hex(hex_string):
    bin_string = bin(int(hex_string, 16))[2:]
    bin_string = '0' * ((4-len(bin_string)) % 4) + bin_string
    counter = 0
    while hex_string[counter] == "0":
        bin_string = 4*'0' + bin_string
        counter += 1
    return decompose_binary_string(bin_string)


def apply_operation(operation, output_list):
    if operation == 4:
        return output_list

    values = [apply_operation(t, o) for (v, t, o) in output_list]
    if operation == 0:
        return sum(values)
    elif operation == 1:
        return prod(values)
    elif operation == 2:
        return min(values)
    elif operation == 3:
        return max(values)
    elif operation == 5:
        return int(values[0] > values[1])
    elif operation == 6:
        return int(values[0] < values[1])
    elif operation == 7:
        return int(values[0] == values[1])


if __name__ == "__main__":
    text = common.import_file('input/day16_input').split('\n')[0]
    output_list = decompose_hex(text)
    print(f"Part 1: {output_list[-1]}")
    to_compute = output_list[0][0]
    print(f"Part 2: {apply_operation(to_compute[1], to_compute[2])}")