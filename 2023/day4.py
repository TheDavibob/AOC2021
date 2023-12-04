import common


def parse_input(input):
    winning_nos_dict = {}
    draws_dict = {}
    for line in input.split("\n"):
        if line == "":
            continue

        card_id, details = line.split(": ")
        id = int(card_id[4:])

        winning_nos, draws = details.split(" | ")
        winning_nos_list = [int(x) for x in winning_nos.split(" ") if x != ""]
        draws_list = [int(x) for x in draws.split(" ") if x != ""]

        winning_nos_dict[id] = winning_nos_list
        draws_dict[id] = draws_list

    return winning_nos_dict, draws_dict


def part_one(winning_nos, draws):
    score = 0
    for key, winning_nos in winning_nos.items():
        wins = set(winning_nos).intersection(draws[key])
        if len(wins) > 0:
            score += 2**(len(wins)-1)

    common.part(1, score)


def part_two(winning_nos, draws):
    card_count = {ID: 1 for ID in winning_nos.keys()}
    total_cards = 0
    for key, winning_nos in winning_nos.items():
        n_cards = card_count[key]
        total_cards += n_cards
        wins = set(winning_nos).intersection(draws[key])
        for idx_shift in range(len(wins)):
            card_count[key + idx_shift + 1] += n_cards

    common.part(2, total_cards)


if __name__ == "__main__":
    input = common.import_file("input/day4")
#     input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    out = parse_input(input)
    part_one(*out)
    part_two(*out)