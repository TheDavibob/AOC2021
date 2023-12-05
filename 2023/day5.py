import common

def parse_input(text):
    blocks = text.split("\n\n")
    seeds = [int(seed) for seed in blocks[0].split(" ")[1:]]

    output = []
    for block in blocks[1:]:
        lines = block.split("\n")
        from_to = lines[0].split(" ")[0]
        f = from_to.split("-")[0]
        t = from_to.split("-")[-1]

        each_entry = []
        for line in lines[1:]:
            each_entry.append(tuple(int(x) for x in line.split(" ")))

        output.append((f, t, each_entry))

    return seeds, output


def part_one(seeds, info):
    exit_states = []
    for seed in seeds:
        # print(f"{seed=}")
        current_loc = seed

        for block in info:
            has_updated = False
            for line in block[-1]:
                if (current_loc >= line[1]) and current_loc < (line[1] + line[2]):
                    has_updated = True
                    current_loc = line[0] + (current_loc - line[1])
                    break

            if not has_updated:
                current_loc = current_loc

            # print(current_loc)

        exit_states.append(current_loc)

    common.part(1, min(exit_states))


def part_two(seeds, info):
    new_seeds = [(x, y) for (x, y) in zip(seeds[::2], seeds[1::2])]
    for info_bits in info:
        block = info_bits[-1]
        new_seeds = split_seeds(new_seeds, block)

    common.part(2, min([x[0] for x in new_seeds]))

    return new_seeds


def split_seeds(seeds, block):
    # seeds is a list of tuples (start, len)
    # blocks is a list of tuples (dest, source start, len)

    # for any blocks seeds overlap with, split seeds

    new_seeds = []
    for seed in seeds:
        new_seed = split_seed(seed, block)
        new_seeds = new_seeds + new_seed
    return new_seeds


def split_seed(seed, block):
    remaining = seed

    new_seeds = []
    for mapping in block:
        if remaining is None:
            break
        remaining, new = single_split_seed(remaining, mapping)
        if new:
            new_seeds.append(new)

    if remaining:
        new_seeds.append(remaining)

    return new_seeds


def single_split_seed(seed, mapping):
    start, length = seed
    stop = start + length - 1

    dest, source_start, source_length = mapping
    source_stop = source_start + source_length - 1
    if start > source_stop:
        remaining_seed = seed
        new_seed = None
        return remaining_seed, new_seed

    if stop < source_start:
        remaining_seed = seed
        new_seed = None
        return remaining_seed, new_seed

    if start >= source_start and stop <= source_stop:
        new_start = start - source_start + dest

        remaining_seed = None
        new_seed = (new_start, length)
        return remaining_seed, new_seed

    elif start >= source_start:
        remaining_seed = (source_stop+1, stop-source_stop)

        new_start = start - source_start + dest
        new_length = length - (stop-source_stop)
        new_seed = (new_start, new_length)
        return remaining_seed, new_seed
    else:
        remaining_seed = (start, source_start - start - 1)
        new_length = length - (source_start - start)

        new_seed = (dest, new_length)
        return remaining_seed, new_seed

if __name__ == "__main__":
    text = common.import_file("input/day5")
#     text="""seeds: 79 14 55 13
#
# seed-to-soil map:
# 50 98 2
# 52 50 48
#
# soil-to-fertilizer map:
# 0 15 37
# 37 52 2
# 39 0 15
#
# fertilizer-to-water map:
# 49 53 8
# 0 11 42
# 42 0 7
# 57 7 4
#
# water-to-light map:
# 88 18 7
# 18 25 70
#
# light-to-temperature map:
# 45 77 23
# 81 45 19
# 68 64 13
#
# temperature-to-humidity map:
# 0 69 1
# 1 0 69
#
# humidity-to-location map:
# 60 56 37
# 56 93 4"""

    seeds, info = parse_input(text)

    exit_states = part_one(seeds, info)
    new_seeds = part_two(seeds, info)
