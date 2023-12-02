with open("input/day1") as file:
    text = file.read()

total = 0
for line in text.split("\n"):
    for char in line:
        if char.isnumeric():
            leading = char
            break

    for char in line[::-1]:
        if char.isnumeric():
            trailing = char
            break

    number = int(leading + trailing)
    total += number

print(f"Part 1: {total}")


numbers_3 = {
    "one": "1",
    "two": "2",
    "six": "6",
}
numbers_4 = {
    "four": "4",
    "five": "5",
    "nine": "9",
}
numbers_5 = {
    "three": "3",
    "seven": "7",
    "eight": "8"
}


total = 0
for line in text.split("\n"):
    leading = None
    for i, char in enumerate(line):
        if char.isnumeric():
            if leading is None:
                leading = char

            trailing = char
        elif (three := line[i:i+3]) in numbers_3.keys():
            if leading is None:
                leading = numbers_3[three]
            trailing=numbers_3[three]
        elif (four := line[i:i+4]) in numbers_4.keys():
            if leading is None:
                leading = numbers_4[four]
            trailing=numbers_4[four]
        elif (five := line[i:i+5]) in numbers_5.keys():
            if leading is None:
                leading = numbers_5[five]
            trailing=numbers_5[five]

    number = int(leading + trailing)
    total += number

print(f"Part 2: {total}")