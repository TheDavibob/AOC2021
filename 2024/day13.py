from copy import deepcopy


def parse_input(text):
    games = []
    for block in text.split("\n\n"):
        line0, line1, line2, *_ = block.split("\n")

        bits = []
        for line in line0, line1, line2:
            _, useful = line.split(": ")
            x, y = useful.split(", ")
            x = int(x[2:])
            y = int(y[2:])
            bits.append((x, y))

        game = {
            "A": bits[0],
            "B": bits[1],
            "GOAL": bits[2],
        }
        games.append(game)

    return games


def solve_game(game):
    # aAx + bBx = Gx
    # aAy + bBy = Gy
    # ((Ax, Bx), (Ay, By)) (a, b) = G
    # 1/(AxBy-AyBx) ((By, -Bx), (-Ay, Ax)) G = (a, b)
    # a = D (ByGx - BxGy)  ; b = D (-AyGx + AxGy)

    A = game["A"]
    B = game["B"]
    goal = game["GOAL"]
    det = A[0] * B[1] - A[1] * B[0]

    a_unscaled = B[1] * goal[0] - B[0] * goal[1]
    b_unscaled = -A[1] * goal[0] + A[0] * goal[1]

    if a_unscaled % det != 0:
        return None
    if b_unscaled % det != 0:
        return None

    a_presses = a_unscaled // det
    b_presses = b_unscaled // det
    return a_presses, b_presses


if __name__ == "__main__":
    with open("input/day13") as file:
        text = file.read()

#     text = """Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400
#
# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176
#
# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=7870, Y=6450
#
# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=18641, Y=10279"""

    games = parse_input(text)

    score = 0
    for game in games:

        game_score = solve_game(game)
        if game_score:
            score += 3 * game_score[0] + game_score[1]

    # 103040 is too high
    print(f"Part 1: {score}")


    score = 0
    for game in games:
        new_game = deepcopy(game)
        new_game["GOAL"] = tuple(x + 10000000000000 for x in game["GOAL"])
        game_score = solve_game(new_game)
        if game_score:
            score += 3 * game_score[0] + game_score[1]

    print(f"Part 2: {score}")