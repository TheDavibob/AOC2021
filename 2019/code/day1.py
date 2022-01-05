import common

text = common.import_file("../input/day1")
list_of_ints = common.return_int_list(text)

total_sum = 0
for mass in list_of_ints:
    total_sum += mass // 3 - 2

print(f"Part 1: {total_sum}")

total_sum = 0
for mass in list_of_ints:
    new_mass = mass // 3 - 2
    while new_mass > 0:
        total_sum += new_mass
        new_mass = new_mass // 3 - 2

print(f"Part 2: {total_sum}")
