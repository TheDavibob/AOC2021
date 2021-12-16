import numpy as np
import networkx as nx
import common

def create_graph(grid):
    """
    Create a graph which connects adjacent grid cells - note that the forwards and backwards weights are different.
    """
    G = nx.DiGraph()
    size = grid.shape[0]
    for i in range(size):
        for j in range(size):
            G.add_node((i, j))

    for i in range(size - 1):
        for j in range(size):
            G.add_edge((i, j), (i + 1, j), weight=grid[i + 1, j])

    for i in range(size - 1):
        for j in range(size):
            G.add_edge((i + 1, j), (i, j), weight=grid[i, j])

    for i in range(size):
        for j in range(size - 1):
            G.add_edge((i, j), (i, j + 1), weight=grid[i, j + 1])

    for i in range(size):
        for j in range(size - 1):
            G.add_edge((i, j+1), (i, j), weight=grid[i, j])

    return G


def extend_grid(grid):
    height, width = grid.shape
    extended_grid = np.zeros((5*height, 5*width), dtype=int)
    for i in range(5):
        for j in range(5):
             # The grid lies between 1 and 9 - so to use mod, find grid - 1 between 0-8 and add 1
            extended_grid[i*height:(i+1)*height, j*width:(j+1)*width] = np.mod(grid + i + j - 1, 9) + 1

    return extended_grid


if __name__ == "__main__":
    text = common.import_file('input/day15_input')

    grid = common.convert_string_to_np_array(text, {str(i): i for i in range(10)})

    G = create_graph(grid)
    shortest_path = nx.shortest_path_length(G, source=(0, 0), target=(grid.shape[0] - 1, grid.shape[1] - 1), weight='weight')
    print(f"Part 1: {shortest_path}")

    ext_grid = extend_grid(grid)
    G = create_graph(ext_grid)
    shortest_path = nx.shortest_path_length(G, source=(0, 0), target=(ext_grid.shape[0] - 1, ext_grid.shape[1] - 1), weight='weight')
    print(f"Part 2: {shortest_path}")