with open("input/day1") as file:
    text = file.read()

list0 = []
list1 = []

for line in text.split("\n"):
    if line == "":
        continue
    el0, el1 = line.split("   ")

    list0.append(int(el0))
    list1.append(int(el1))

s0 = sorted(list0)
s1 = sorted(list1)

d = sum(abs(a - b) for a, b in zip(s0, s1))
print(f"Part 1: {d}")

locs = tuple(s1)

total = 0
for target in s0:
    count = locs.count(target)
    total += count * target

print(f"Part 2: {total}")