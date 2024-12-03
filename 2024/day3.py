import re

with open("input/day3") as file:
    text = file.read()


def sum_block(text):
    matches = re.findall("mul\([0-9]{1,3},[0-9]{1,3}\)", text)
    total = 0
    for match in matches:
        a, b = match.split(",")
        num0 = int(a.split("(")[-1])
        num1 = int(b.split(")")[0])

        total += num0 * num1
    return total

print(f"Part 1: {sum_block(text)}")

donts = text.split("don't")
total = sum_block(donts[0])
for block in donts[1:]:
    guff, *dos = block.split("do")
    for sublock in dos:
        total += sum_block(sublock)

print(f"Part 2: {total}")
