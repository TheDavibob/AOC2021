import numpy as np
import common

def blocks(array):
    index_array = np.zeros(array.shape, dtype=int)

    # This number is the first that has not yet been used to label a block
    next_available_integer = 1

    # Loop over all points
    for i_row in range(index_array.shape[0]):
        for i_col in range(index_array.shape[1]):
            if array[i_row, i_col] == 9:
                # Peak: label -1 and continue
                index_array[i_row, i_col] = -1
            else:
                # Get the value above and to the left, that
                # have already been filled in
                if i_row > 0:
                    above = index_array[i_row-1, i_col]
                else:
                    above = 0

                if i_col > 0:
                    left = index_array[i_row, i_col - 1]
                else:
                    left = 0

                if (left > 0) and (above > 0) and (left != above):
                    # Two values for the same block: join them
                    # together and carry on
                    index_array[index_array == above] = left
                    index_array[i_row, i_col] = left
                elif left > 0:
                    index_array[i_row, i_col] = left
                elif above > 0:
                    index_array[i_row, i_col] = above
                else:
                    # Unlabelled block: assign the next available value
                    index_array[i_row, i_col] = next_available_integer
                    next_available_integer = next_available_integer + 1

    return index_array


if __name__ == "__main__":
    text = common.import_file('input/day9_input')
    array = common.convert_string_to_np_array(text, {str(t): t for t in range(10)})

    # Create a mask which is True if the point of interest is smaller than all surrounding points
    low_mask = np.ones(array.shape, dtype=bool)
    low_mask[:, :-1] *= array[:, :-1] < array[:, 1:]
    low_mask[:, 1:] *= array[:, 1:] < array[:, :-1]
    low_mask[:-1] *= array[:-1] < array[1:]
    low_mask[1:] *= array[1:] < array[:-1]

    print(f"Part 1: {np.sum((array + 1)[low_mask])}")

    # Chop array into blocks, labelled by an integer. Not all integers are used. -1 corresponds to 9s in the
    # original
    labelled_array = blocks(array)

    # Count the size of each block
    block_sizes = np.zeros(np.max(labelled_array), dtype=int)
    for i in range(np.max(labelled_array)):
        block_sizes[i] = np.sum(labelled_array == i)

    # Get the three biggest blocks
    biggest_three_sizes = np.sort(block_sizes)[-3:]

    print(f"Part 2: {biggest_three_sizes[0] * biggest_three_sizes[1] * biggest_three_sizes[2]}")
