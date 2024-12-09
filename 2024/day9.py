import numpy as np

def part_one(text):
    if len(text) % 2 == 1:
        text = text + "0"

    total = sum(int(x) for x in text)
    print(total)

    as_array = np.zeros(total, dtype=int)
    n_slots = len(text) // 2
    current_position = 0
    for i in range(n_slots):
        next_slot = int(text[2*i])
        print(next_slot)
        as_array[current_position:current_position+next_slot] = i
        current_position = current_position + next_slot

        next_gap = int(text[2*i+1])
        print(next_gap)
        as_array[current_position:current_position+next_gap] = -1
        current_position = current_position + next_gap

    assert(current_position == total)

    while np.any(as_array == -1):
        print(np.sum(as_array == -1))
        to_swap = np.where(as_array == -1)[0][0]
        as_array[to_swap] = as_array[-1]
        as_array = as_array[:-1]

    # 6349224763051 is too low
    checksum = 0
    for i, x in enumerate(as_array):
        checksum += int(i) * int(x)

    print(f"Part 1: {checksum}")


def part_two(text):

    # Part 2: we keep the original representation
    blocks = [int(x) for x in text[::2]]
    block_order = [x for x in range(len(blocks))]
    gaps = [int(x) for x in text[1::2]]

    for i in [x for x in range(len(blocks))][::-1]:
        print(i)
        step_part_two(blocks, block_order, gaps, i)

    as_array = np.zeros(sum(blocks) + sum(gaps), dtype=int)
    position = 0
    for block_id, block_length, gap_length in zip(block_order, blocks, gaps + [0,]):
        # block_length = blocks[block_id]
        as_array[position:position+block_length] = block_id
        position = position + block_length

        as_array[position:position+gap_length] = -1
        position = position + gap_length

    # All the gaps appear to be 0 - this is unlikely
    print(as_array)

    # 4906095278354 is too low
    # 6366177999707 is too low
    # 6376613827167 is too low
    checksum = 0
    for i, x in enumerate(as_array):
        if x == -1:
            continue
        checksum += int(i) * int(x)

    print(f"Part 2: {checksum}")


def step_part_two(blocks, block_order, gaps, block_id_to_move):
    block_to_move = block_order.index(block_id_to_move)
    block_length = blocks[block_to_move]

    try:
        next_gap_index, next_gap_length = next(
            (i, g) for i, g in enumerate(gaps) if g >= block_length
        )
    except StopIteration:
        return blocks, block_order, gaps

    if next_gap_index >= block_to_move:
        return blocks, block_order, gaps

    block_order.pop(block_to_move)
    block_order.insert(next_gap_index+1, block_id_to_move)

    blocks.pop(block_to_move)
    blocks.insert(next_gap_index+1, block_length)

    # Make the gap corresponding to this block bigger
    if block_to_move == len(gaps):
        new_gap_length = gaps[block_to_move-1] + block_length
    else:
        new_gap_length = gaps[block_to_move-1] + gaps[block_to_move] + block_length
        gaps.pop(block_to_move)
    gaps[block_to_move - 1] = new_gap_length

    gaps.insert(next_gap_index, 0)
    gaps[next_gap_index + 1] = gaps[next_gap_index + 1]-block_length
    #
    # print(blocks[:10])
    # print(gaps[:10])
    # print(block_order[:10])

    print(sum(gaps) + sum(blocks))  # This should not change
    return blocks, block_order, gaps




if __name__ == "__main__":
    with open("input/day9") as file:
        text = file.read()

    # text = "2333133121414131402"
    # text="12121020102"  # BUG WHEN MOVING ONE SPACE TO THE LEFT ONLY

    # part_one(text)
    part_two(text)
