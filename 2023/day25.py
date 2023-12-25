import sys
from copy import deepcopy

import common


sys.setrecursionlimit(1600)


def parse_input(text):
    graph = {}

    for line in text.split("\n"):
        if line == "":
            continue

        component_from, component_to = line.split(": ")

        if graph.get(component_from, None) is None:
            graph[component_from] = []

        for comp in component_to.split():
            if graph.get(comp, None) is None:
                graph[comp] = [component_from]
            else:
                graph[comp].append(component_from)

            graph[component_from].append(comp)

    return graph


def get_block_size(graph, current_point=None):
    if current_point is None:
        current_point = next(iter(graph.keys()))

    visited = [current_point]
    to_visit = graph[current_point]

    while to_visit:
        next_visit_point = to_visit.pop(0)
        for point in graph[next_visit_point]:
            if point not in visited and point not in to_visit:
                to_visit.append(point)

        visited.append(next_visit_point)

    return len(visited)


def remove_connection(graph, from_con, to_con):
    if to_con == from_con:
        return graph

    if to_con not in graph[from_con]:
        return graph

    graph = deepcopy(graph)
    graph[to_con].remove(from_con)
    graph[from_con].remove(to_con)
    return graph


def brute_force_part_one(graph):
    for to_0 in graph.keys():
        for from_0 in graph.keys():
            print(f"{to_0}:{from_0}")
            if to_0 == from_0:
                continue

            if to_0 not in graph[from_0]:
                continue

            red_0 = remove_connection(graph, to_0, from_0)
            for to_1 in red_0.keys():
                for from_1 in red_0.keys():
                    print(f"\t{to_1}:{from_1}")
                    if to_1 == from_1:
                        continue

                    if to_1 not in graph[from_1]:
                        continue

                    red_1 = remove_connection(graph, to_1, from_1)
                    for to_2 in red_1.keys():
                        for from_2 in red_1.keys():
                            print(f"\t\t{to_2}:{from_2}")
                            if to_2 == from_2:
                                continue

                            if to_2 not in graph[from_2]:
                                continue

                            red_2 = remove_connection(graph, to_2, from_2)

                            if get_block_size(red_2) != len(red_2.keys()):
                                return get_block_size(red_2)


def path_counting(from_point, to_point, visited, graph):
    if from_point == to_point:
        return 1

    head = graph[from_point]
    count = 0
    for point in head:
        if point in visited:
            continue

        count += path_counting(point, to_point, visited + [from_point], graph)

    return count


if __name__ == "__main__":
    text = common.import_file("input/day25")
    graph = parse_input(text)

    nodes = list(graph.keys())
    path_counting(nodes[0], nodes[1], [], graph)

