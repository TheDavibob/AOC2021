import collections


def is_valid(number):
    str_number = str(number)
    in_order = list(str_number) == sorted(str_number)
    count = collections.Counter(str_number)
    repeated_nums = [k for k, v in count.items() if v > 1]

    return in_order and (len(repeated_nums) > 0)


def is_valid_part2(number):
    str_number = str(number)
    in_order = list(str_number) == sorted(str_number)
    count = collections.Counter(str_number)
    repeated_nums = [k for k, v in count.items() if v == 2]

    return in_order and (len(repeated_nums) > 0)


def count_valid(minimum, maximum, validity_fun=is_valid):
    count = 0
    for number in range(minimum, maximum+1):
        if validity_fun(number):
            count += 1
    return count


if __name__ == "__main__":
    print(count_valid(130254, 678275))
    print(count_valid(130254, 678275, validity_fun=is_valid_part2))