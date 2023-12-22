import numpy as np

import common

def parse_input(text):

    segments = []
    for line in text.split("\n"):
        if line == "":
            continue
        (start_point, end_point) = line.split("~")
        start_point = [int(s) for s in start_point.split(",")]
        end_point = [int(e) for e in end_point.split(",")]
        segments.append((start_point, end_point))

    return segments


def check_vertical(segment, segments, n_steps=-1):
    if n_steps < 0:
        this_extreme = min(segment[0][-1], segment[1][-1])
    else:
        this_extreme = max(segment[0][-1], segment[1][-1])

    if this_extreme + n_steps <= 0:
        return True

    for i_other, other in enumerate(segments):
        if segment == other:
            continue

        if n_steps < 0:
            other_extreme = max(other[0][-1], other[1][-1])
        else:
            other_extreme = min(other[0][-1], other[1][-1])

        if other_extreme == this_extreme + n_steps:
            if check_horizontal_overlap(segment, other):
                return True

    return False


def get_support_grid(segments):
    support_matrix = np.zeros((len(segments), len(segments)), dtype=int)
    for i_segment, segment in enumerate(segments):
        # if segment[0][-1] == 1 or segment[1][-1] == 1:
        #     continue

        for j_segment, other_segment in enumerate(segments):
            if check_vertical(segment, [other_segment]):
                support_matrix[i_segment, j_segment] = 1

    return support_matrix


def check_horizontal_overlap(segment_1, segment_2):
    overlaps = []
    for i in range(2):
        start_1, end_1 = segment_1[0][i], segment_1[1][i]
        start_2, end_2 = segment_2[0][i], segment_2[1][i]

        overlap = False
        if end_1 < start_2:
            pass
        elif end_2 < start_1:
            pass
        else:
            overlap = True

        overlaps.append(overlap)

    return all(overlaps)


def fall_segments(segments):
    while True:
        cant_fall = [check_vertical(segment, segments, -1) for segment in segments]
        print(len(segments) - sum(cant_fall))
        if all(cant_fall):
            break

        for i_segment, cant in enumerate(cant_fall):
            if not cant:
                prev_segment = segments[i_segment]
                segments[i_segment] = (
                    prev_segment[0][:2] + [prev_segment[0][2]-1],
                    prev_segment[1][:2] + [prev_segment[1][2]-1],
                )

    return segments


def part_one(segments):
    segments = fall_segments(segments)
    support_matrix = get_support_grid(segments)

    singly_supported = np.sum(support_matrix, axis=-1) == 1
    single_supporters = np.where(support_matrix[singly_supported])[1]
    unique_supporters = np.unique(single_supporters)

    return support_matrix, len(segments) - len(unique_supporters)


def unsupported_if_removed(support_matrix, idx):
    reduced_matrix = support_matrix.copy()

    reduced_matrix[:, idx] = 0
    reduced_matrix[idx, :] = 0

    unsupported_idx = np.where(np.sum(reduced_matrix, axis=1) == 0)[0]

    return reduced_matrix, unsupported_idx


def cascade_unsupported(support_matrix, idx):
    reduced_matrix, unsupported_idx = unsupported_if_removed(support_matrix, idx)

    removed = [idx]
    while len(removed) < len(unsupported_idx):
        next_to_remove = next(unsup for unsup in unsupported_idx if unsup not in removed)

        reduced_matrix, unsupported_idx = unsupported_if_removed(reduced_matrix, next_to_remove)
        removed.append(next_to_remove)

    return len(removed) - 1


def part_two(support_matrix):
    score = 0
    for idx in range(support_matrix.shape[0]):
        score += cascade_unsupported(support_matrix, idx)
        print(f"{idx}/{len(support_matrix)}: {score}")

    return score


if __name__ == "__main__":
    text = common.import_file("input/day22")

    demo_text = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

    demo_segments = parse_input(demo_text)
    support_matrix, score = part_one(demo_segments)

    assert score == 5

    score = part_two(support_matrix)
    assert score == 7

    segments = parse_input(text)
    support_matrix, score = part_one(segments)
    common.part(1, score)
    common.part(2, part_two(support_matrix))
