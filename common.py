from typing import Dict, Optional

import numpy as np


def convert_string_to_np_array(
        input_string: str,
        mapping_dict: Optional[Dict[str, int]]=None):
    """
    If we have a string that consists of a regular grid of characters,
    this is mapped to a numpy array of ints, where all values with the same
    int representation had the same character representation.

    e.g.
    .#.         010
    ###   ->    111
    #.#         101

    Parameters
    ----------
    input_string: str
        Input text, with rows separated by newline characters
    mapping_dict: Dict[str, int]
        Mapping from characters to integers. If not provided, automatically
        generated starting from 0.

    Returns
    -------
    np.ndarray
        dtype=int

    """
    lines = [line for line in input_string.split('\n') if line != '']

    len_line = len(lines[0])
    for line in lines:
        assert len(line) == len_line, 'Not all the lines are the same length'

    out_array = np.zeros((len(lines), len_line), dtype=int)

    character_list = set(''.join(lines))
    if mapping_dict is None:
        mapping_dict = {}
        for i_char, char in enumerate(character_list):
            mapping_dict[char] = i_char
    else:
        # Fill up mapping dict with any missing characters
        new_val = 0
        for char in character_list:
            if char in mapping_dict.keys():
                continue

            while new_val in mapping_dict.values():
                new_val += 1

            mapping_dict[char] = new_val

    for row, line in enumerate(lines):
        for column, character in enumerate(line):
            out_array[row, column] = mapping_dict[character]

    return out_array


def return_int_list(string: str) -> np.ndarray:
    """
    Convert a string, consisting of integers on each row, to a list of ints,
    cast to a numpy array.

    Parameters
    ----------
    string: text list of integers (separated by newlines)

    Returns
    -------
    np.ndarray

    """
    return np.array([int(num) for num in string.split('\n') if num != ''])


def import_file(filepath: str) -> str:
    """
    Load a file as a string. New lines are represented by the newline character.

    Parameters
    ----------
    filepath: str

    Returns
    -------
    text: str

    """
    with open(filepath) as file:
        text = file.read()

    return text


def from_binary_array(bool_array: np.ndarray) -> int:
    """
    Converts a numpy boolean array (1-d) to an integer
    e.g. [1, 0, 0, 1] -> 8 + 1 = 9

    Parameters
    ----------
    bool_array: np.ndarray, shape=(n,), dtype = bool

    Returns
    -------
    int
    """
    return np.sum(2**np.arange(len(bool_array))[::-1] * bool_array)


def part(part_no, answer):
    print(f"Part {part_no}: {answer}")


def load_input(day):
    return import_file("../input/day" + str(day))


def single_dijkstra(distance_dict, filled_nodes):
    """

    distance_dict: Dict[node, distance: int]
    filled_node: List[node]
    """
    unfilled_neighbours = {}
    for edge, distance in distance_dict.items():
        if (edge[0] in filled_nodes.keys()) and (edge[1] not in filled_nodes.keys()):
            neighbour = edge[1]
            if unfilled_neighbours.get(neighbour, None) is None:
                unfilled_neighbours[neighbour] = distance + filled_nodes[edge[0]]
            else:
                unfilled_neighbours[neighbour] = min(distance + filled_nodes[edge[0]], unfilled_neighbours[neighbour])

    new_neighbour = min(unfilled_neighbours, key=unfilled_neighbours.get)
    filled_nodes[new_neighbour] = unfilled_neighbours[new_neighbour]
    return filled_nodes, new_neighbour


def flood_fill(grid_array, source):
    distance = np.inf*np.ones_like(grid_array, dtype=float)
    distance[source] = 0
    current_value = 0

    neighbour_directions = (
        [0, 1],
        [1, 0],
        [-1, 0],
        [0, -1]
    )

    while np.any(np.isinf(distance[grid_array > 0])):
        # Find all edge values
        edge_values = np.where(distance == current_value)
        if len(edge_values[0]) == 0:
            break
        for i, j in zip(*edge_values):
            for direction in neighbour_directions:
                neighbour_position = tuple(np.array([i, j]) + np.array(direction))
                if grid_array[neighbour_position] == 0:
                    continue
                if not np.isinf(distance[neighbour_position]):
                    continue

                distance[neighbour_position] = current_value + 1

        current_value += 1

    return distance
