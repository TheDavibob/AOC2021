import common


def parse_input(input):
    text = common.import_file(input)

    games = text.split("\n")
    game_list = {}
    for game in games:
        if game == "":
            continue
        game_id, game_deets = game.split(": ")

        game_number = int(game_id[5:])

        draws = game_deets.split("; ")
        draw_list = []
        for draw in draws:
            draw_dict = {"r": 0, "g": 0, "b": 0}
            individual_draws = draw.split(", ")
            for individual_draw in individual_draws:
                number, color = individual_draw.split(" ")
                # if color in ("red", "green", "blue"):
                draw_dict[color[0]] = int(number)
            draw_list.append(draw_dict)
        game_list[game_number] = draw_list

    return game_list


def part_one(game_list):
    target_r = 12
    target_g = 13
    target_b = 14

    games_included = []
    for game_id, game_deets in game_list.items():
        max_color = {"r": 0, "g": 0, "b": 0}
        for draw in game_deets:
            max_color["r"] = max(draw["r"], max_color["r"])
            max_color["g"] = max(draw["g"], max_color["g"])
            max_color["b"] = max(draw["b"], max_color["b"])

        if (max_color["r"] <= target_r) and (max_color["g"] <= target_g) and (max_color["b"] <= target_b):
            games_included.append(game_id)

    common.part(1, sum(games_included))


def part_two(game_list):
    powers = []
    for game_id, game_deets in game_list.items():
        max_color = {"r": 0, "g": 0, "b": 0}
        for draw in game_deets:
            max_color["r"] = max(draw["r"], max_color["r"])
            max_color["g"] = max(draw["g"], max_color["g"])
            max_color["b"] = max(draw["b"], max_color["b"])

        power = max_color["r"] * max_color["g"] * max_color["b"]
        powers.append(power)

    common.part(2, sum(powers))


if __name__ == "__main__":
    game_list = parse_input("input/day2")
    part_one(game_list)
    part_two(game_list)
