import functools

from tqdm import tqdm


def parse_input(text):
    first, second = text.split("\n\n")
    words = first.split(", ")
    targets = [x for x in second.split("\n") if x != ""]
    return words, targets


@functools.cache
def ways_to_make(target):
    print(target)
    if target == "":
        return 1

    n_ways = 0
    for word in words:
        if len(word) > len(target):
            # Assumes words are sorted
            break
        if target[:len(word)] == word:
            n_ways += ways_to_make(target[len(word):])

    return n_ways


def can_make(target):
    if target in words:
        return True

    this_can = False
    for word in words:
        if target[:len(word)] == word:
            this_can |= can_make(target[len(word):])

        if this_can:
            break

    return this_can


if __name__ == "__main__":
    with open("input/day19") as file:
        text = file.read()

    words, targets = parse_input(text)
    words = sorted(words, key=len)

    part_one = 0
    for target in tqdm(targets):
        part_one += can_make(target)
    print(f"Part 1: {part_one}")

    part_two = 0
    for target in tqdm(targets):
        n_ways = ways_to_make(target)
        part_two += n_ways
    print(f"Part 2: {part_two}")