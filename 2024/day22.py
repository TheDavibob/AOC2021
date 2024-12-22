from itertools import product

from tqdm import tqdm


def step(number):
    tester = number << 6
    number = mix_and_prune(number, tester)

    tester = number >> 5
    number = mix_and_prune(number, tester)

    tester = number << 11
    number = mix_and_prune(number, tester)

    return number


def mix_and_prune(number, alternative):
    return (number ^ alternative) % (2**24)


def step_n(number, n):
    for _ in range(n):
        number = step(number)
    return number


def step_n_and_store_differences(number, n):
    numbers = [number]
    diffs = []
    for _ in range(n):
        new_number = step(number)
        numbers.append(new_number % 10)
        diffs.append((new_number % 10) - (number % 10))
        number = new_number
    return numbers, diffs


def calc_value(nums, diffs, sequence):
    pos = 0
    for i, d in enumerate(diffs):
        if sequence[pos] == d:
            pos += 1
        else:
            pos = 0

        if pos == 4:
            return nums[i+1]

    return 0


def find_sequences(diffs):
    sequences = []
    for d in tqdm(diffs):
        for i in range(0, len(d)-4):
            sequence = d[i:i+4]
            if sequences not in sequences:
                sequences.append(sequence)
                print(len(sequences))

    return sequences


def calc_all_scoring_sequences(nums, diffs):
    vals = {}
    for i in range(0, len(diffs)-4):
        sequence = tuple(diffs[i:i+4])
        if sequence not in vals:
            vals[sequence] = nums[i+4]

    return vals


if __name__ == "__main__":
    with open("input/day22") as file:
        text = file.read()

    # total = 0
    # for line in text.split("\n"):
    #     if line == "":
    #         continue
    #     total += step_n(int(line), 2000)
    #
    # print(f"Part 1: {total}")

#     text = """1
# 2
# 3
# 2024"""

    numbers = []
    differences = []
    for line in text.split("\n"):
        if line == "":
            continue
        nums, diffs = step_n_and_store_differences(int(line), 2000)
        numbers.append(nums)
        differences.append(diffs)

    # seqeuences = find_sequences(differences)

    # best_banan = 0
    # for sequence in product(*4*[list(range(-9, 10))]):
    #     valid_sequence = True
    #     s_total = 0
    #     for s in sequence:
    #         s_total += s
    #         if s_total >= 10:
    #             valid_sequence = False
    #             break
    #         if s_total <= -10:
    #             valid_sequence = False
    #             break
    #
    #     if not valid_sequence:
    #         continue
    #
    #     tv = 0
    #     for n, d in zip(numbers, differences):
    #         tv += calc_value(n, d, sequence)
    #
    #     if tv > best_banan:
    #         best_banan = tv
    #
    #     print(sequence, best_banan, tv)

    vals = []
    for n, d in tqdm(zip(numbers, differences)):
        vals.append(calc_all_scoring_sequences(n, d))

    all_sequences = set()
    for v in tqdm(vals):
        all_sequences = all_sequences.union(v.keys())

    best_score = 0
    sequence_score = {}
    for sequence in tqdm(all_sequences):
        score = 0
        for v in vals:
            if sequence in v:
                score += v[sequence]

        if score > best_score:
            best_score = score
        print(sequence, best_score, score)
        sequence_score[sequence] = score

    # 2176 is too low