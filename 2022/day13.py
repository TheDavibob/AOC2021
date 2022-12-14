import numpy as np
import common


def parse_input(text):
    blocks = []
    for block in text.split("\n\n"):
        line0, line1 = block.split("\n")[:2]
        left = eval(line0)
        right = eval(line1)
        blocks.append((left, right))

    return blocks


def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return -1
        elif a > b:
            return 1
        else:
            return 0

    if isinstance(a, int):
        a = [a]
    if isinstance(b, int):
        b = [b]

    for i in range(max(len(a), len(b))):
        try:
            A = a[i]
        except IndexError:
            return -1

        try:
            B = b[i]
        except IndexError:
            return 1

        out = compare(A, B)
        if out == 1:
            return 1
        elif out == -1:
            return -1
        else:
            pass

    return 0


def sort(packets):
    is_changed = True
    while is_changed:
        is_changed = False
        for i_packet in range(len(packets)-1):
            if compare(packets[i_packet], packets[i_packet+1]) == 1:
                packets[i_packet:i_packet+2] = packets[i_packet:i_packet+2][::-1]
                is_changed = True

    return packets


example_text = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""


if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    # text = example_text
    blocks = parse_input(text)

    index_sum = 0
    for i_block, block in enumerate(blocks):
        if compare(*block) == -1:
            index_sum += (i_block+1)

    common.part(1, index_sum)

    packets = [[[2]], [[6]]]
    for block in blocks:
        packets.append(block[0])
        packets.append(block[1])

    packets = sort(packets)

    common.part(2, (packets.index([[2]])+1) * (packets.index([[6]])+1))
