from itertools import permutations

import common


def parse_input(text):
    mood_dict = {}
    for line in text.split('\n'):
        if line == "":
            continue
        source, _, sign, count, *_, target = line.split(' ')

        if sign == "gain":
            value = int(count)
        elif sign == "lose":
            value = -int(count)

        mood_dict[(source, target[:-1])] = value
    return mood_dict


def get_permutation_quality(mood_dict, permutation):
    quality = 0
    for i in range(len(permutation)):
        quality += mood_dict[(permutation[i], permutation[i-1])]
        quality += mood_dict[(permutation[i-1], permutation[i])]
    return quality


def get_best_permutation_qualities(mood_dict):
    people = {k[0] for k in mood_dict.keys()}
    best_quality = -100000
    for p in permutations(people):
        quality = get_permutation_quality(mood_dict, p)
        if quality > best_quality:
            best_quality = quality

    return best_quality

if __name__ == "__main__":
    text = common.load_input(13)
    mood_dict = parse_input(text)
    common.part(1, get_best_permutation_qualities(mood_dict))

    people = {k[0] for k in mood_dict.keys()}
    for person in people:
        mood_dict[('me', person)] = 0
        mood_dict[(person, 'me')] = 0

    common.part(2, get_best_permutation_qualities(mood_dict))