# /// script
# dependencies = [
# ]
# ///

with open("data/day_01") as file:
    data = file.read()

test_data = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""

# data = test_data

commands = []
for line in data.split("\n"):
    if line != "":
        commands.append(line)


def step(num, command):
    if command[0] == "L":
        num -= int(command[1:])
        num %= 100

    elif command[0] == "R":
        num += int(command[1:])
        num %= 100

    return num


num = 50
all_nums = [num]
for command in commands:
    num = step(num, command)
    all_nums.append(num)

print(len(all_nums))
print(f"Part 1: {len([n for n in all_nums if n == 0])}")


def step_click(num, command):
    click = 0
    if command[0] == "L":
        num *= -1
        num %= 100
        num += int(command[1:])

        if num >= 100:
            click += (num // 100)

        num *= -1
        num %= 100

    elif command[0] == "R":
        num += int(command[1:])
        if num >= 100:
            click += (num // 100)
            num %= 100

    return num, click


num = 50
all_nums = [num]
all_clicks = 0
for command in commands:
    num, click = step_click(num, command)
    all_nums.append(num)
    all_clicks += int(click)

# 3245 too low
print(f"Part 2: {all_clicks}")

# Debugging
print(step_click(99, "L1000"))
#
# print(int(0x434C49434B))