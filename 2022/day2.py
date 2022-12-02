import numpy as np
import common

THEM = {
    "A": 0,
    "B": 1,
    "C": 2
}

YOU = {
    "X": 0,
    "Y": 1,
    "Z": 2
}

RESULT = {
    "X": -1,
    "Y": 0,
    "Z": 1
}

if __name__ == "__main__":
    text = common.import_file("input/day2")

    score = 0
    for line in text.split('\n'):
        if line != "":
            them, you = line.split(' ')
            them = THEM[them]
            you = YOU[you]

            if (you - them) % 3 == 1:
                score += 6
            elif you == them:
                score += 3

            score += (you + 1)

    common.part(1, score)

    score = 0
    for line in text.split('\n'):
        if line != "":
            them, result = line.split(' ')
            them = THEM[them]

            if result == "X":
                you = (them - 1) % 3
                score += 0
            elif result == "Y":
                you = them
                score += 3
            elif result == "Z":
                you = (them + 1) % 3
                score += 6
            else:
                you = 0

            score += (you + 1)

    common.part(2, score)
