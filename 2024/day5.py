with open("input/day5") as file:
    text = file.read()

# text = """47|53
# 97|13
# 97|61
# 97|47
# 75|29
# 61|13
# 75|53
# 29|13
# 97|29
# 53|29
# 61|53
# 97|53
# 61|29
# 47|13
# 75|47
# 97|75
# 47|61
# 75|61
# 47|29
# 75|13
# 53|13
#
# 75,47,61,53,29
# 97,61,53,29,13
# 75,29,13
# 75,97,47,61,53
# 61,13,29
# 97,13,75,29,47
# """

first, second = text.split("\n\n")
valid_map = []
for line in first.split("\n"):
    before, after = line.split("|")
    valid_map.append((int(before), int(after)))

sequences = []
for line in second.split("\n"):
    if line == "":
        continue
    sequences.append([int(x) for x in line.split(",")])


total = 0
for sequence in sequences:
    valid = True
    for i_char, char in enumerate(sequence):
        for a, b in valid_map:
            if char == b:
                if a in sequence[i_char+1:]:
                    valid = False
                    break

        if not valid:
            break

    if valid:
        total += sequence[len(sequence) // 2]

print(f"Part 1: {total}")

total = 0
for sequence in sequences:
    complete = True
    
    valid = True
    for i_char, char in enumerate(sequence):
        for a, b in valid_map:
            if char == b:
                if a in sequence[i_char+1:]:
                    valid = False
                    break

        if not valid:
            break

    complete = valid
    if complete:
        print("Skipping as complete")
        continue
        
    while not complete:
        valid = True
        for i_char, char in enumerate(sequence):
            for a, b in valid_map:
                if char == b:
                    if a in sequence[i_char + 1:]:
                        valid = False
                        sequence[i_char + sequence[i_char:].index(a)] = b
                        sequence[i_char] = a
                        break

            if not valid:
                break
        
        complete = valid

    total += sequence[len(sequence) // 2]

# 3968 too low
print(f"Part 2: {total}")