import numpy as np
import common


SNAFU_MAP = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2
}

REVERSE_SNAFU_MAP = {v: k for k, v in SNAFU_MAP.items()}

def snafu_to_dec(snafu_str):
    dec_no = 0

    for i, char in enumerate(str(snafu_str)[::-1]):
        snafu_rep = SNAFU_MAP[char]
        dec_no += (5**i) * snafu_rep

    return dec_no


def dec_to_snafu(num: int):
    snafu_rep = ""
    i = 0
    while True:
        if (i > 0) and (num < 5**(i-1)):
            break

        shifted = int(num) + 2*5**i
        downscaled = (shifted // 5**i)
        pow_5 = downscaled % 5
        snafu_rep = snafu_rep + REVERSE_SNAFU_MAP[pow_5-2]

        num -= (pow_5-2) * 5**i

        i += 1

    return snafu_rep[::-1]


if __name__ == "__main__":
    text = common.load_todays_input(__file__)

    total = 0
    for line in text.split("\n"):
        total += snafu_to_dec(line)

    common.part(1, dec_to_snafu(total))

    common.part(2, "Merry Christmas!")
