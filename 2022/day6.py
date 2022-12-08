import numpy as np
import common


def start_of_packet(text, n_chars):
    line = text.split("\n")[0]
    for n in range(len(line)-n_chars+1):
        nos = set(line[n:n+n_chars])
        if len(nos) == n_chars:
            return n + n_chars

    return np.nan


if __name__ == "__main__":
    text = common.load_todays_input(__file__)

    common.part(1, start_of_packet(text, 4))

    common.part(2, start_of_packet(text, 14))
