def parse_input(text):
    challenges = []
    for line in text.split("\n"):
        if line == "":
            continue

        target, components = line.split(": ")
        target = int(target)
        components = [int(x) for x in components.split(" ")]
        challenges.append((target, components))

    return challenges


def solve_part_one_challenge(challenge):
    target, components = challenge
    score_so_far = [components[0]]
    for component in components[1:]:
        new_scores = []
        for score in score_so_far:
            new_scores.append(score + component)
            new_scores.append(score * component)

        score_so_far = new_scores

    return target in score_so_far


def part_one(challenges):
    total = 0
    for challenge in challenges:
        if solve_part_one_challenge(challenge):
            total += challenge[0]

    print(f"Part 1: {total}")



def solve_part_two_challenge(challenge):
    target, components = challenge
    score_so_far = [components[0]]
    for component in components[1:]:
        new_scores = []
        for score in score_so_far:
            new_scores.append(score + component)
            new_scores.append(score * component)
            new_scores.append(int(str(score) + str(component)))

        score_so_far = new_scores

    return target in score_so_far


def part_two(challenges):
    total = 0
    for challenge in challenges:
        if solve_part_two_challenge(challenge):
            total += challenge[0]

    print(f"Part 1: {total}")


if __name__ == "__main__":
    with open("input/day7") as file:
        text = file.read()

#     text = """190: 10 19
# 3267: 81 40 27
# 83: 17 5
# 156: 15 6
# 7290: 6 8 6 15
# 161011: 16 10 13
# 192: 17 8 14
# 21037: 9 7 18 13
# 292: 11 6 16 20"""

    challenges = parse_input(text)
    part_one(challenges)
    part_two(challenges)


