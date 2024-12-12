import numpy as np

import common


def to_single_blocks(region_array):
    new_array = -1 * np.ones_like(as_array)
    next_available_number = 0
    for i in range(new_array.shape[0]):
        for j in range(new_array.shape[1]):
            # Look above, ignore variable names
            if i == 0:
                left_neighbour = False
            elif region_array[i-1, j] == region_array[i, j]:
                left_neighbour = True
            else:
                left_neighbour = False

            if j == 0:
                above_neighbour = False
            elif region_array[i, j-1] == region_array[i, j]:
                above_neighbour = True
            else:
                above_neighbour = False

            if left_neighbour:
                if above_neighbour:
                    new_array[i, j] = new_array[i, j-1]
                    new_array[new_array == new_array[i-1, j]] = new_array[i, j-1]
                else:
                    new_array[i, j] = new_array[i-1, j]
            elif above_neighbour:
                new_array[i, j] = new_array[i, j - 1]
            else:
                new_array[i, j] = next_available_number
                next_available_number += 1

    return new_array



def find_n_fences_for_region(map_array, region_id):
    region = map_array == region_id
    region_indices = np.where(region)
    xs = region_indices[0]
    ys = region_indices[1]
    fences = []
    for x, y in zip(xs, ys):
        fences.extend(find_fences_for_single_point(map_array, (x, y)))
    return fences


def find_fences_for_single_point(region_array, coordinate):
    fences = []
    for direction in (([0, 1], [1, 0], [-1, 0], [0, -1])):
        new_direction = (
            coordinate[0] + direction[0],
            coordinate[1] + direction[1],
        )

        if (
            (new_direction[0] < 0)
            or (new_direction[1] < 0)
            or (new_direction[0] >= region_array.shape[0])
            or (new_direction[1] >= region_array.shape[1])
        ):
            fences.append((coordinate, direction))

        elif region_array[new_direction] != region_id:
            fences.append((coordinate, direction))

    return fences


def prune_fences(fence_list):
    # Remove fence if a coordinate to the above or to the left has a fence
    # with the same direction
    kept_fences = []
    for fence in fence_list:
        fence_coordinate, fence_direction = fence
        keep = True
        for other_fence in fence_list:
            other_coordinate, other_direction = other_fence
            if other_direction != fence_direction:
                continue

            if other_coordinate == (fence_coordinate[0] - 1, fence_coordinate[1]):
                keep = False
            elif other_coordinate == (fence_coordinate[0], fence_coordinate[1]-1):
                keep = False
            if not keep:
                break

        if keep:
            kept_fences.append(fence)

    return kept_fences



if __name__ == "__main__":
    with open("input/day12") as file:
        text = file.read()

#     text="""AAAA
# BBCD
# BBCC
# EEEC"""

#     text = """OOOOO
# OXOXO
# OOOOO
# OXOXO
# OOOOO"""

    as_array = common.convert_string_to_np_array(text)
    as_array = to_single_blocks(as_array)

    score = 0
    for region_id in np.unique(as_array):
        fences = find_n_fences_for_region(as_array, region_id)
        print(f"{region_id}, {len(fences)}")
        score += np.sum(as_array == region_id) * len(fences)

    # 2018890 is too high
    print(f"Part 1: {score}")

    score = 0
    for region_id in np.unique(as_array):
        fences = find_n_fences_for_region(as_array, region_id)
        print(f"{region_id}, {len(fences)}")
        fences = prune_fences(fences)
        print(f"{region_id}, {len(fences)}")
        score += np.sum(as_array == region_id) * len(fences)

    # 1238455 is too high
    print(f"Part 2: {score}")