import common

input = common.load_input(8)

cumulative = 0
for line in input.split('\n'):
    if line == "":
        continue
    print(line, eval(line))
    line_len = len(line)
    repr_len = len(eval(line))
    cumulative += (line_len - repr_len)

common.part(1, cumulative)

cumulative = 0
for line in input.split('\n'):
    if line == "":
        continue

    cumulative += 2
    for s in line:
        if ord(s) in [34, 39, 92]:
            cumulative += 1

common.part(2, cumulative)