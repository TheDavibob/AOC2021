import common


def split_into_blocks_and_update(integer_as_str):
    blocks = []
    current_block = integer_as_str[0]
    for s in integer_as_str[1:]:
        if s == current_block[-1]:
            current_block = current_block + s
        else:
            blocks.append(current_block)
            current_block = s
    blocks.append(current_block)

    new_blocks = []
    for block in blocks:
        new_blocks.append(str(len(block)) + block[0])

    return "".join(new_blocks)


def loop(input, n=40):
    current_str = str(input)
    for _ in range(n):
        current_str = split_into_blocks_and_update(current_str)

    return current_str


if __name__ == "__main__":
    common.part(1, len(loop(1113222113, 40)))
    common.part(2, len(loop(1113222113, 50)))