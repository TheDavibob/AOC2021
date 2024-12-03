import numpy as np

with open("input/day2") as file:
    text = file.read()

levels = []
for line in text.split("\n"):
    if line == "":
        continue

    levels.append(
        np.array([int(x) for x in line.split(" ")], dtype=int)
    )


def is_safe(level):
    diffs = np.diff(level)
    if np.any(np.abs(diffs) > 3):
        return False

    return (np.all(diffs > 0) or np.all(diffs < 0))


n_safe = 0
for level in levels:
    n_safe += is_safe(level)

print(f"Part 1: {n_safe}")


def is_safe_2(level):
    if is_safe(level):
        return True

    for i in range(len(level)):
        if is_safe(np.hstack((level[:i], level[i+1:]))):
            return True

    return False


n_safe = 0
for level in levels:
    n_safe += is_safe_2(level)

print(f"Part 2: {n_safe}")