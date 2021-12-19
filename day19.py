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


def compute_offset(pairmap):
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

    for d in pairmap:
        # Points in first frame
        x0, y0 = d[0]

        # Points in second frame
        x1, y1 = d[1]

        # First: get pair of possible permutations/signs by looking at in frame distances
        d0 = x0 - y0
        d1 = x1 - y1

        if d0[0] in d0[1:]:
            continue
        elif d0[1] == d0[2]:
            continue

        candidate_permutation, candidate_sign = None, None
        for permutation in positive_permutations:
            for sign in positive_signs:
                d1_p = np.array([d1[p] for p in permutation])*sign
                if np.all(d1_p == d0):
                    candidate_permutation = permutation
                    candidate_sign = sign
                    swap = False
                elif np.all(d1_p == -d0):
                    candidate_permutation = permutation
                    candidate_sign = sign
                    swap = True
                    break
            if candidate_permutation:
                break

        for permutation in negative_permutations:
            for sign in negative_signs:
                d1_p = np.array([d1[p] for p in permutation])*sign
                if np.all(d1_p == d0):
                    candidate_permutation = permutation
                    candidate_sign = sign
                    swap = True
                elif np.all(d1_p == -d0):
                    candidate_permutation = permutation
                    candidate_sign = sign
                    swap = False
                    break
            if candidate_permutation:
                break

        if swap:
            candidate = y1
        else:
            candidate = y0

        inverse_permutation = [np.arange(3)[p] for p in candidate_permutation]
        offset = [(x0*candidate_sign)[p] for p in inverse_permutation] - candidate

    return offset, candidate_permutation, candidate_sign


def append_to_block(block0, block1):
    overlap = get_overlap(block0, block1)
    if len(overlap) == 0:
        print("No overlap")

    print(f"{len(overlap)} points overlap")
    offset, perm, sign = compute_offset(overlap)

    new_block_0 = list(block0)
    for b in block1:
        rotated = np.array([b[p] for p in perm])*sign
        new_block_0.append(rotated + offset)

    print(len(new_block_0))
    new_block_0 = np.unique(new_block_0, axis=0)
    print(len(new_block_0))
    return new_block_0


def construct_all_maps(text):
    blocks = []
    for block in text.split('\n\n'):
        blocks.append(construct_scanner_map(block))

    return blocks


if __name__ == "__main__":
    text = common.import_file('input/day19_input')
    blocks = construct_all_maps(text)
    overlap = get_overlap(blocks[0], blocks[7])
    # block = append_to_block(blocks[0], blocks[7])
