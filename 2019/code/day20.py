import numpy as np
import networkx as nx

import common
from day18 import flood_fill


def str_to_grid(grid_str, outside_to_wall=True, label_interior=False):
    letter_dict = {chr(i+65): i+100 for i in range(26)}
    grid = common.convert_string_to_np_array(grid_str, {" ": -1, "#": 0, ".": 1} | letter_dict)

    for i in range(1, grid.shape[0]-1):
        for j in range(1, grid.shape[1] - 1):
            if grid[i, j] > 1:
                directions = (
                    (0, 1),
                    (1, 0),
                    (0, -1),
                    (-1, 0)
                )
                for d in directions:
                    neighbour = tuple(np.array([i, j]) + np.array(d))
                    other_neighbour = tuple(np.array([i, j]) - np.array(d))
                    if (grid[neighbour] > 1) and grid[other_neighbour] == 1:
                        if label_interior:
                            if (neighbour[0] in (0, grid.shape[0] - 1)) or (neighbour[1] in (0, grid.shape[1] - 1)):
                                # exterior point
                                append_label = '1'
                            else:
                                #interior point
                                append_label = '2'
                        else:
                            append_label = ''
                        if np.any(np.array(d) > 0):
                            grid[i, j] = int(append_label + str(grid[i, j]) + str(grid[neighbour]))
                        else:
                            grid[i, j] = int(append_label + str(grid[neighbour]) + str(grid[i, j]))
                        grid[neighbour] = -1
                        break

    if outside_to_wall:
        grid[grid == -1] = 0

    return grid


def get_distance_from_point_to_others(grid, source):
    source_distance = {}
    distance = flood_fill(grid, source)
    values = np.unique(grid[grid > 1])
    for value in values:
        value_location = np.where(grid == value)
        if np.any(~np.isinf(distance[value_location])):
            source_distance[value] = int(np.min(distance[value_location])) - 1

    return source_distance


def get_full_distance_dict(grid):
    full_distance_dict = {}
    sources = np.unique(grid[grid > 1])
    for source in sources:
        source_location = np.where(grid == source)
        for i, j in zip(*source_location):
            source_distance = get_distance_from_point_to_others(grid, (i, j))
            for k, v in source_distance.items():
                if source == k:
                    continue
                full_distance_dict[(source, k)] = v

    return full_distance_dict


def get_networkx_graph(full_distance_dict):
    g = nx.DiGraph()
    for nodes, distance in full_distance_dict.items():
        for node in nodes:
            if node in g.nodes:
                g.add_node(node)
        g.add_edge(nodes[0], nodes[1], weight=distance)
    return g


def single_dijkstra(distance_dict, filled_nodes):
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


def dijkstra_part_1(distance_dict):
    start = 100100
    end = 125125
    filled_nodes = {start: 0}
    while end not in filled_nodes.keys():
        filled_nodes, _ = single_dijkstra(distance_dict, filled_nodes)

    return filled_nodes[end] - 1


def add_layer_to_distance_dict(layered_distance_dict, base_distance_dict, layer):
    for (source, target), distance in base_distance_dict.items():
        source_reduced = int(str(source)[1:])
        target_reduced = int(str(target)[1:])
        if target_reduced in [100100, 125125]:  # i.e. is A or Z - this don't exit on outer layers
            if layer == 0:
                layered_distance_dict[((source, layer), (target, layer))] = distance
            continue

        if source_reduced in [100100, 125125] and layer != 0:
            continue

        is_exterior = str(target)[0] == '1'

        # Target is the inner/exterior version of the apparent target
        if str(target)[0] == "1":
            target = int("2" + str(target_reduced))
        else:
            target = int("1" + str(target_reduced))

        if is_exterior:
            # exterior point
            if layer - 1 < 0:
                continue
            else:
                layered_distance_dict[((source, layer), (target, layer-1))] = distance
        else:
            layered_distance_dict[((source, layer), (target, layer+1))] = distance

    return layered_distance_dict


def dijkstra_part_2(distance_dict):
    # Grid must have interior / exterior appended
    start = (1100100, 0)
    end = (1125125, 0)

    # Need a function that adds an n-1 to all interior points, and an n+1 to all
    # exterior points: probably actually when creating the dict.
    layered_distance_dict = {}
    add_layer_to_distance_dict(layered_distance_dict, distance_dict, 0)

    filled_nodes = {start: 0}
    added_layers = [0]
    while end not in filled_nodes.keys():
        filled_nodes, new_node = single_dijkstra(layered_distance_dict, filled_nodes)
        if new_node[1] not in added_layers:
            add_layer_to_distance_dict(layered_distance_dict, distance_dict, new_node[1])
            added_layers.append(new_node[1])

    return filled_nodes[end] - 1



if __name__ == "__main__":
    grid_str = """                                   H     C       O         L   Q     X   U                                         
                                   W     N       V         H   G     H   P                                         
  #################################.#####.#######.#########.###.#####.###.#######################################  
  #...#...#.#.......#...................#.#...#.....#.#.#...#.......#...#.....#...#.......#...........#.......#.#  
  ###.#.###.###.###.#####.#####.#######.#.#.#.#####.#.#.#.###.#.#.#####.#.#####.###.#.#.###.###.#####.###.#####.#  
  #.......#.#.....#...#...#.#...#...#...#...#...#.#.....#.....#.#.#.....#.......#...#.#.......#.....#.#.#.#.#...#  
  #.#.#.###.#####.#.#.#####.###.#.#.#.#.#.#.###.#.#####.#######.###.#.#.###.#######.#####.#####.#######.#.#.###.#  
  #.#.#...#...#...#.#.........#.#.#...#.#.#.#.#.#.......#.....#...#.#.#.#...........#...#...#.#...#.......#.....#  
  #######.#.#######.#.###.#.#####.###########.#.#.###.###.###.#.#####.#######.#.#####.###.###.###########.###.###  
  #.........#.#...#.#.#.#.#...............#.....#...#...#...#...#.#.......#...#.#.#.#...#.#.#.#.#.....#.#.......#  
  #########.#.###.###.#.#############.#########.#.#######.###.#.#.#.###.###.#.###.#.#.#####.#.#.#.#####.#.###.#.#  
  #.#...#.....#.#.......#...#.#.........#...#...#...#...#.#...#.#.#...#...#.#.#...#.#...#.#.#.........#...#...#.#  
  #.###.###.#.#.###.#.#####.#.###.###.#.#.###.#.#.#####.#.###.###.#.#######.###.###.#.###.#.#.###########.###.###  
  #.#.#.....#.#...#.#.#...........#...#.#.....#.#...#.......#.#.........#.....#.#.........#...#.#.#.#.....#.....#  
  #.#.#.###.#####.#######.###.###.###.###.#.#.###.#.###.###.#####.#.#####.###.#.#.#.#.###.#.###.#.#.#########.###  
  #.....#.#.#.#.#.......#.#...#.....#...#.#.#.#...#...#.#.......#.#.#.#.....#.....#.#...#.............#.#.#.....#  
  #######.#.#.#.#######.#.#######.#######.#######.#.#####.#######.###.#########.#####.#.#.#####.#.###.#.#.#.#.###  
  #...........#.....#...#...#.#...#.#.#.......#...#.#.........#.#...#...#.#...#.#...#.#.#.....#.#.#.#.#...#.#.#.#  
  ###########.#####.#.#######.###.#.#.###.###.###.###.#.#.#.###.#.###.###.###.#.#.###.#######.#.###.###.#####.#.#  
  #...#.........#...#.#.#.....#.....#...#.#...#...#.#.#.#.#.....#.#.#.......#.....#.......#.#.#.#.#.#...#...#.#.#  
  ###.###.#.#.###.#.#.#.###.#####.###.#.#.###.###.#.###########.#.#.#.#######.#.#####.#####.#####.#.###.###.#.#.#  
  #.......#.#...#.#.........#.#...#.#.#.#.#.#.#.#...#.#.#.......#.#.......#.#.#.#.#.#.#.#...........#.....#.#...#  
  #####.#####.###.#.#.#####.#.###.#.#.###.#.#.#.#.#.#.#.#.###.#.#.###.#.###.###.#.#.###.#####.#########.#.#.#.###  
  #.....#.#.....#.#.#...#.....#...#.....#...#.#...#.....#...#.#.#.....#.#.#.............#.#...#.#.....#.#.......#  
  #.#.###.#.#.#############.#####.#.###.###.###########.###.#######.###.#.#.#######.#####.#.#.#.#####.###.###.###  
  #.#.#.....#...#...#...#.#...#.#...#...#.......#.....#.#.......#...#...#.........#.....#.#.#.#.....#...#.#.....#  
  ###########.###.#####.#.#.###.#.###.###.#.#.###.#.###.#.#######.#.###.###.###.#.###.###.#.###.#####.#######.###  
  #.#.....#.#.....#.#.#.#...#.....#.....#.#.#.#.#.#.#...#.#.#.#.#.#.#...#...#...#...#.....#...#.#.#.....#.....#.#  
  #.###.###.###.#.#.#.#.###.###########.#.#####.#.#.#.#.#.#.#.#.#######.###.###.#########.#.#.#.#.###.#.#.#####.#  
  #.#.#...#...#.#.#.#.#.#.#.......#.....#.....#...#...#.#.........#.......#...#.........#.#.#.#...#.#.#...#.#.#.#  
  #.#.###.###.###.#.#.#.#.#.#########.#####.#####.#######.#.#########.#########.###########.#####.#.###.#.#.#.#.#  
  #.#.#.........#.#.#.#...#...#      O     X     C       H C         O         U    #.....#.#.#...#...#.#.#.#.#.#  
  #.#.#######.###.#.#.#.###.###      V     H     D       W N         M         D    ###.###.#.###.###.###.#.#.#.#  
  #...................#.......#                                                     #.#.......#.#.#...#.....#...#  
  #####.###.###.#.#.#.#.###.#.#                                                     #.#.###.#.#.#.###.#####.###.#  
  #.#...#.....#.#.#.#...#.#.#..VW                                                 CA..#.#...#...............#....UD
  #.#######.###.#.###.#.#.#.#.#                                                     #.#######.###########.###.#.#  
PW..#.......#.#.#.#...#.#...#.#                                                     #.#.........#...........#.#.#  
  #.###.###.#.###########.###.#                                                     #.#.#.###.#######.#######.###  
  #.......#.........#...#.#...#                                                     #.#.#.#...#...#...#...#.#...#  
  #######.#.###.#######.#######                                                     #.#.#####.#.#####.#.#.#.#.###  
  #.#...#.#.#...#.........#...#                                                     #.....#.#.#.#...#...#.......#  
  #.#.#######.#####.###.#####.#                                                     #######.###.#.###############  
CD..#.#.#...#.#.#.....#.#.#.#..KT                                                 QD......#...#.................#  
  #.#.#.###.###.#####.#.#.#.#.#                                                     #####.#.#.#.###.###.#.###.###  
  #.....#...#.#.......#.....#.#                                                     #.....#.#...#.....#.#.#.....#  
  #.#.#####.#.#.#.###.#.#.#.#.#                                                     #.#.###.#.#.###.###.#.###.#.#  
  #.#...........#...#.#.#.#...#                                                     #.#.#...#.#...#...#.#.#.#.#..GK
  ###########################.#                                                     #.###.#.#####.#.#######.###.#  
  #.....................#.#...#                                                     #.....#...#.#.#...#.#.....#.#  
  #.#####.#.#####.#.###.#.#####                                                     #######.###.#######.###.#.###  
  #...#.#.#...#...#...#.....#.#                                                     #.....#.#...#.......#.#.#...#  
  ###.#.###.#####.#.###.###.#.#                                                     #.###.#####.###.#.#.#.#####.#  
  #.#.....#.#.#...#.#...#.#.#.#                                                   AI..#.#.....#.....#.#.#...#....MO
  #.###.#####.#######.#.#.#.#.#                                                     #.#.#####.#.###.###.#.#####.#  
VW............#.#...#.#.#......XU                                                   #.#...#.......#.#.........#.#  
  ###.#.#.#####.###.###########                                                     ###.###.###########.#####.#.#  
  #...#.#.....#.#.#.......#...#                                                     #.....#.#.#...#...#.#...#...#  
  #########.###.#.#.#.#.###.#.#                                                     #.###.#.#.#.###.#####.#######  
OM....#.#.#.#...#...#.#.#.#.#.#                                                     #.#...#.#.......#.......#...#  
  #.###.#.#####.###.#####.#.#.#                                                     ###.#.###.###.###.#####.#.#.#  
  #...#...#...#.....#.#.....#.#                                                     #...#...#...#.....#.#.#...#..ZL
  ###.#.#.###.#.###.#.#####.#.#                                                     ###.###.#.###.#####.#.###.#.#  
  #.#...#.......#...........#..TD                                                 MO......#...#.#...#.#...#...#.#  
  #.#####################.#####                                                     ###########.#####.#.#########  
  #...................#...#...#                                                     #...................#...#...#  
  #.#####.#.#.#.#####.#####.#.#                                                     ###.#.###.###.#####.###.#.#.#  
  #.....#.#.#.#...#.#.#.#...#.#                                                     #...#.#...#.....#.....#.#.#.#  
  #####.#####.#.###.#.#.###.#.#                                                     #.#.#.#############.###.#.#.#  
AF....#...#.#.#...#.........#.#                                                   GD..#.#.#.#...#...#.........#..KT
  #.#.#.###.###.#####.#######.#                                                     #######.###.###.#######.#####  
  #.#.....#...#.#...#.#.#...#..UP                                                 GK....#.#...............#.#...#  
  ###.#####.#####.###.#.#.###.#                                                     #.#.#.###.###.#.###.#######.#  
  #...#...#...#.....#.#.....#.#                                                     #.#...#.....#.#...#.....#.#.#  
  #####.###.###.#########.#.###                                                     ###.#.#.#####.#.###.###.#.#.#  
  #...#.#.#.....#.....#.#.#...#                                                     #...#.#.....#.#.#...#...#....RC
  #.###.#.#.###.###.#.#.#.###.#                                                     #####.#.#############.#####.#  
  #...#.#.....#.#...#.#.....#.#                                                     #.#.......#.....#.#.#.......#  
  #.###.#####.#.#.###.#.#.###.#                                                     #.#.#.###.#.###.#.#.#######.#  
ZE............#.....#...#...#..LH                                                   #.#.#.#.#.#.#.......#...#...#  
  #.#.#################.#######                                                     #.#####.#########.#.#.#.#####  
  #.#...#.#.#.....#.#.#.#.....#                                                     #.#.#.........#.#.#...#.....#  
  #######.#.#.#.#.#.#.#.###.#.#                                                     #.#.###.#.#.###.#.#######.###  
  #...........#.#.#...#.#...#..JN                                                 AF..#...#.#.#.#.#...#.....#.#..JN
  #####.#######.###.#######.###                                                     #.#.###.#.###.###.#.###.#.#.#  
  #...........#.....#...#.#...#                                                     #.......#.........#.#.......#  
  #########.#####.###.###.#.###                                                     #.#.#####.#######.###.###.#.#  
QD..............#.............#                                                     #.#.#...........#.#.....#.#.#  
  #.#.###.###.#####.#.###.###.#      Q           Z       R   P           R   Z      #####.###.#######.#######.###  
  #.#.#.#.#.......#.#.#.#.#...#      G           L       C   W           Y   E      #...#.#.....#.#...#.........#  
  #.###.#.#.#.#######.#.#.#.#.#######.###########.#######.###.###########.###.#######.###.###.#.#.#.#.###.###.#.#  
  #...#...#.#.#...#.....#.#.#...#.........#.......#...#...#.....#.........#.........#...#.#...#.#.#.#.#...#...#.#  
  #.###.#.#####.###.#.#######.###.###.#.#####.###.#.###.###.#####.#.#####.###.#.#.###.#######.###.#.#.###.###.#.#  
  #...#.#...#.#...#.#...#.....#...#...#...#...#.#.#...#.#.#...#.#.#.#...#.#...#.#...........#...#...#.#...#...#.#  
  #.#.###.###.#.#####.#######.###.#####.###.###.###.#.#.#.###.#.###.#.###########.#.#.#############.#.###.#.#.#.#  
  #.#.#.......#...#.....#.......#.#.#...#.......#...#.....#.#...#.....#.#...#.....#.#...#.#.#.#.....#.#...#.#.#.#  
  #.###.#.#.#####.###.#.###.#.#####.#.#####.#.#####.#######.#.#######.#.#.#####.#.#.###.#.#.#.###.###.###.#.###.#  
  #...#.#.#...#.......#.#...#.#.#...#.....#.#...#.#.....#.........#.....#.#.#...#.#...#.......#...#.....#.#...#.#  
  #.#######.###.#.###.#########.#.#.#.###.###.#.#.#.#.#####.###.#####.###.#.#.#.###.#####.#.#.###.###.#####.#####  
  #.....#...#...#...#...#.......#.#.#.#.....#.#.#.#.#.#.#.....#.#.......#.....#.#.......#.#.#...#.#.#.#.....#...#  
  #.#.#.###.#.###.###.###.#####.#.#.###.#.###.###.#.#.#.###.#####.#.###.###.#######.#####.#########.#.###.#.###.#  
  #.#.#...#.#...#.#.....#.#.......#.....#.#...#.#.#.#.....#.#.....#.#...#.....#.#.....#.#...#.......#.#...#.....#  
  #.###.#.###.###.#.#.#.#####.#####.#####.#.###.#.#######.#.#####.#.#######.###.#######.#######.###.###.#.#.#####  
  #.#...#.#.#...#.#.#.#.#.....#.#.......#.#.#.#...........#.#.#...#...#.........#.......#.#.......#.#.#.#.#.....#  
  #.#.#.###.#.###.#####.###.###.###.#######.#.#########.###.#.#####.###.###.#########.###.###.#####.#.#####.#.#.#  
  #.#.#.#.......#.#.....#.#.#...........#.....#...#.#.....#...#.#.....#.#...#...........#.....#.#.#.#...#...#.#.#  
  #.#######.#######.#.###.#.#######.#.#.###.#####.#.###.###.###.###.#######.#######.#####.###.#.#.###.#####.#####  
  #.....#...#.......#.....#.#.#.#...#.#.#.#...#.....#.#...#...#...#.#.#.#.#.#.....#.........#.....#.....#.#.#...#  
  #.#.#.#.#.###.#.###########.#.###.#.#.#.#.###.###.#.###.#.#####.#.#.#.#.#.#.#####.#####.#####.#.#.###.#.#.###.#  
  #.#.#.#.#...#.#.#.#.......#.......#.#.#.........#.#.....#...#.#...#.....#...........#.#.....#.#.....#.#.......#  
  #.###.###.#.#####.#######.###.###.#########.###.#####.#.#.###.###.###.#.#######.#.#.#.###.###.#.#########.#.###  
  #.#...#.#.#...#.#.#.#.#.........#.#...#.......#.#...#.#.#.......#...#.#.#.....#.#.#.#...#...#.#.#.....#...#...#  
  #######.#.#.#.#.#.#.#.###########.###.###.#####.#.#####.###.###.###.#.#.#.#.###.#.###.#.#########.#######.#.###  
  #.....#...#.#.#.....#.....#.#.........#.......#.#.........#.#...#.....#.#.#.....#.....#.#...#.........#.#.#...#  
  ###.#.###.#######.###.#.#.#.#.#.#.###.#######.#######.###.###.#########.#.###.#.#.#.#.###.#######.###.#.###.###  
  #...#...........#.....#.#.....#.#...#...#...#.#...#.#...#.#.....#.......#...#.#.#.#.#.....#.#.......#.....#...#  
  #.#.###.#.#.#.#####.###.#.#.#####.###.#.#.#.#.#.#.#.#.#######.#####.#.#.###.#.#.###.#.###.#.###.#.#########.#.#  
  #.#.#...#.#.#.#.......#.#.#.#.....#...#.#.#.....#.#.......#...#.....#.#.#...#.#...#.#...#.......#.........#.#.#  
  ###################################.#####.#########.#.#######.###.#.#####.#####################################  
                                     X     T         Z A       C   G A     R                                       
                                     U     D         Z I       A   D A     Y                                       
"""
    grid = str_to_grid(grid_str)
    full_distance_dict = get_full_distance_dict(grid)
    common.part(1, dijkstra_part_1(full_distance_dict))

    grid = str_to_grid(grid_str, label_interior=True)
    full_distance_dict = get_full_distance_dict(grid)
    common.part(2, dijkstra_part_2(full_distance_dict))
