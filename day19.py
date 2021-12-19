import numpy as np
import matplotlib.pyplot as plt

import common


def construct_scanner_map(scan_block):
    coords = []
    for line in scan_block.split('\n')[1:]:
        if line != "":
            coords.append([int(l) for l in line.split(',')])

    coords = np.array(coords, dtype=int)

    return coords


def get_pairwise_distances(block):
    euc_squared = np.sum((block[None, :, :] - block[:, None, :])**2, axis=2)
    manhattan = np.sum(np.abs(block[None, :, :] - block[:, None, :]), axis=2)
    l_inf = np.max(np.abs(block[None, :, :] - block[:, None, :]), axis=2)
    l_0 = np.min(np.abs(block[None, :, :] - block[:, None, :]), axis=2)

    return np.array([l_0, manhattan, euc_squared, l_inf])


def get_overlap(block0, block1):
    D0 = get_pairwise_distances(block0)
    D1 = get_pairwise_distances(block1)

    pairmap = []
    for row0 in range(D0.shape[1]):
        for col0 in range(row0+1, D0.shape[2]):
            candidate_distances = D0[:, row0, col0]
            for row1 in range(D1.shape[1]):
                for col1 in range(row1 + 1, D1.shape[2]):
                    if np.all(candidate_distances == D1[:, row1, col1]):
                        pairmap.append(
                            [[block0[row0], block0[col0]], [block1[row1], block1[col1]]]
                        )

    return np.array(pairmap)


def reduce_overlap(overlap):
    coords_in_frame_0 = np.unique(
        np.vstack([d[0] for d in overlap]),
        axis=0
    )
    coords_in_frame_1 = np.unique(
        np.vstack([d[1] for d in overlap]),
        axis=0
    )

    tuple_0 = tuple(tuple(c) for c in coords_in_frame_0)
    tuple_1 = tuple(tuple(c) for c in coords_in_frame_1)

    mapping = dict()
    for c in tuple_0:
        possibles = set(tuple_1)
        for d in overlap:
            if c in d[0]:
                new_possibles = tuple(tuple(e) for e in d[1])
                possibles = possibles.intersection(new_possibles)
        if len(possibles) == 0:
            continue
        else:
            mapping[c] = next(iter(possibles))

    return mapping


def map_to_block0(mapping, block1):
    frame_0 = np.array([k for k, v in mapping.items()])
    frame_1 = np.array([v for k, v in mapping.items()])

    d0 = frame_0[1] - frame_0[0]
    d1 = frame_1[1] - frame_1[0]

    positive_permutations = [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
    positive_signs = [
        np.array([1, 1, 1]),
        np.array([-1, -1, 1]),
        np.array([1, -1, -1]),
        np.array([-1, 1, -1]),
    ]

    negative_permutations = [(0, 2, 1), (1, 0, 2), (2, 1, 0)]
    negative_signs = [
        np.array([-1, -1, -1]),
        np.array([-1, 1, 1]),
        np.array([1, -1, 1]),
        np.array([1, 1, -1]),
    ]

    candidate = None
    for perm in positive_permutations:
        if candidate is not None:
            break

        for sign in positive_signs:
            if np.all(np.array([d1[p] for p in perm])*sign == d0):
                candidate = perm, sign
                break

    for perm in negative_permutations:
        if candidate is not None:
            break

        for sign in negative_signs:
            if np.all(np.array([d1[p] for p in perm]) * sign == d0):
                candidate = perm, sign
                break

    # Then: frame_0 = frame_0[0] + (frame_1-frame_1[0])[:, candidate[0]] * candidate[1]
    block1_in_frame_0 = (
        frame_0[0] + (block1 - frame_1[0])[:, candidate[0]] * candidate[1]
    )
    return block1_in_frame_0


def append_to_block(block0, block1):
    overlap = get_overlap(block0, block1)
    if len(overlap) == 0:
        # print("No overlap")
        return block0, False

    mapping = reduce_overlap(overlap)
    # print(f"{len(mapping)} points overlap")
    block1_0 = map_to_block0(mapping, block1)

    extended_block_0 = np.unique(np.vstack((block0, block1_0)), axis=0)
    print(len(extended_block_0))
    return extended_block_0, True


def construct_all_maps(text):
    blocks = []
    for block in text.split('\n\n'):
        blocks.append(construct_scanner_map(block))

    return blocks


def main(blocks):
    block = blocks[0]
    length_so_far = len(block)
    blocks_done = [False for _ in range(len(block))]
    blocks_done[0] = True

    while True:
        for i, (b, done) in enumerate(zip(blocks, blocks_done)):
            if not done:
                block, success = append_to_block(block, b)
                if success:
                    done += 1
                    print(f"Added block {i}")

        if all(done):
            break
        length_so_far = len(block)
        print(f'Iterated, length = {length_so_far}')

    print(f"Final length: {length_so_far}")
    return block


if __name__ == "__main__":
    text = common.import_file('input/day19_input')
    blocks = construct_all_maps(text)
    block = main(blocks)
