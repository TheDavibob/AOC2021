import math

import common

def parse_input(text):
    lines = text.split("\n")
    cards_bids = []
    for line in lines:
        if line == "":
            continue
        cards, bids = line.split(" ")
        cards_bids.append((cards, int(bids)))

    return cards_bids


def get_card_type(card, with_joker=False):
    if with_joker:
        n_jokers = card.count("J")
        card = card.replace("J", "")
    else:
        n_jokers = 0

    if n_jokers == 5:
        return 0

    chars = []
    count = []
    for char in card:
        if char in chars:
            continue
        else:
            chars.append(char)
            count.append(card.count(char))

    maxi = max(count) + n_jokers
    if maxi == 5:
        return 0
    elif maxi == 4:
        return 1
    elif maxi == 3 and len(count) == 2:
        return 2
    elif maxi == 3:
        return 3
    elif maxi == 2 and len(count) == 3:
        return 4
    elif maxi == 2:
        return 5
    else:
        return 6


def part(cards_bids, part_no=1):
    if part_no == 2:
        jokers = True
    else:
        jokers = False

    sorted_list = []
    for card, bid in cards_bids:
        insertion_point = None
        for i, (sorted_card, sorted_bin) in enumerate(sorted_list):
            if greater_than(sorted_card, card, with_jokers=jokers):
                insertion_point = i
                break

        if insertion_point is None:
            sorted_list.append((card, bid))
        else:
            sorted_list.insert(insertion_point, (card, bid))

    score = 0
    for i_card, (card, bid) in enumerate(sorted_list):
        score += (i_card+1) * bid

    common.part(part_no, score)

    return sorted_list


def greater_than(card_0, card_1, with_jokers=False):
    type_0 = get_card_type(card_0, with_jokers)
    type_1 = get_card_type(card_1, with_jokers)

    if type_0 < type_1:
        return True
    if type_0 > type_1:
        return False

    for char_0, char_1 in zip(card_0, card_1):
        if char_to_num(char_0, with_joker=with_jokers) > char_to_num(char_1, with_joker=with_jokers):
            return True
        elif char_to_num(char_0, with_joker=with_jokers) < char_to_num(char_1, with_joker=with_jokers):
            return False

    return False


CHAR_MAP = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
CHAR_MAP_J = {"T": 10, "J": 1, "Q": 12, "K": 13, "A": 14}
VAL_MAP = {0: "FIVE", 1: "FOUR", 2: "FULL", 3: "THREE", 4: "2PAIR", 5: "PAIR", 6: "NONE"}


def char_to_num(char, with_joker=False):
    if char.isnumeric():
        return int(char)
    else:
        if with_joker:
            return CHAR_MAP_J[char]
        else:
            return CHAR_MAP[char]


if __name__ == "__main__":
    text = common.import_file("input/day7")
#     text="""32T3K 765
# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483"""
    parsed_input = parse_input(text)
    part(parsed_input, 1)
    sl = part(parsed_input, 2)
