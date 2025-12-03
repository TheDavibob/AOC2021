def to_even_string(number):
    as_str = str(number)
    if len(as_str) % 2 == 1:
        as_str = "0" + as_str
    return as_str


def split_even_str(as_str):
    len_split = len(as_str) // 2
    return int(as_str[:len_split]), int(as_str[len_split:])


def count_invalid_ids(smallest, largest, debug=False):
    smallest_str = to_even_string(smallest)
    largest_str = to_even_string(largest)

    s1, s2 = split_even_str(smallest_str)

    id_sum = 0
    init_value = min(s1, s2)
    while True:
        test = int(str(init_value) + str(init_value))
        if test >= smallest and test <= largest:
            id_sum += test
            if debug:
                print(test)

        if test >= largest:
            break

        init_value += 1

    return id_sum


def split_n_string(number, n):
    if len(str(number)) % n == 0:
        full_str = str(number)
    else:
        zeros_to_prepend = n - (len(str(number)) % n)
        full_str = "0" * zeros_to_prepend + str(number)

    n_stride = len(full_str) // n

    split = tuple(full_str[i*n_stride:(i+1)*n_stride] for i in range(n))
    return split


def count_in_range_iterative(smallest, largest, debug=False):
    max_n = len(str(largest))
    id_sum = 0
    seen_so_far = set()
    for n in range(2, max_n+1):
        smallest_split = split_n_string(smallest, n)
        if debug:
            print(smallest_split, n)
        init_value = min(int(s) for s in smallest_split)
        while True:
            test = int(n*str(init_value))
            if test >= smallest and test <= largest:
                if test not in seen_so_far:
                    id_sum += test
                    if debug:
                        print(test)
                    seen_so_far.add(test)

            if test >= largest:
                break

            init_value += 1

    return id_sum



def run_on_input(input_str):
    id_sum = 0
    for value in input_str.split(","):
        start, end = value.split("-")
        id_sum += count_invalid_ids(int(start), int(end))

    return id_sum


def run_on_input_iterative(input_str, debug=False):

    id_sum = 0
    for value in input_str.split(","):
        start, end = value.split("-")
        new_count = count_in_range_iterative(int(start), int(end), debug=debug)
        id_sum += new_count
        if debug:
            print(value, new_count)

    return id_sum


if __name__ == "__main__":
    test_input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
    assert run_on_input(test_input) == 1227775554

    with open("data/day_02") as f:
        real_input = f.read()

    print("Part 1:", run_on_input(real_input))

    assert run_on_input_iterative(test_input) == 4174379265

    print("Part 2:", run_on_input_iterative(real_input))