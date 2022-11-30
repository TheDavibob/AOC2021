import common


def string_to_int(string):
    power = 0
    value = 0
    for s in string[::-1]:
        value += 26**power * (ord(s) - 97)
        power += 1

    return value


def int_to_string(integer, string_length=8):
    s = ""
    for _ in range(string_length):
        i = integer % 26
        s = chr(i + 97) + s
        integer = integer // 26

    return s


triplets = [chr(i) + chr(i+1) + chr(i+2) for i in range(97, 97+24)]
invalid_letters = ["i", "o", "l"]
pairs = [chr(i) + chr(i) for i in range(97, 97+26)]

def is_valid(string):
    for l in invalid_letters:
        if l in string:
            valid = False
            return valid

    contains_triplet = False
    for t in triplets:
        if t in string:
            contains_triplet = True
            break

    pair_count = 0
    for p in pairs:
        if p in string:
            pair_count += 1
            if pair_count == 2:
                break

    return (pair_count == 2) and contains_triplet


def increment_until_find_password(initial_password):
    password_as_int = string_to_int(initial_password)
    valid = False
    while not valid:
        password_as_int += 1
        string_int = int_to_string(password_as_int, len(initial_password))

        for l in invalid_letters:
            if l in string_int:
                split_index = next(i for i, j in enumerate(string_int) if j == l)
                string_int = string_int[:split_index] + chr(ord(l) + 1) + 'a'*(len(initial_password) - split_index - 1)
                password_as_int = string_to_int(string_int)

        valid = is_valid(string_int)

    return string_int


if __name__ == "__main__":
    password1 = increment_until_find_password('cqjxjnds')
    common.part(1, password1)
    password2 = increment_until_find_password(password1)
    common.part(2, password2)
