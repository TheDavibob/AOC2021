import sys

import numpy as np
import networkx as nx

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


def get_edges(graph):
    nodes = list(graph.keys())
    edge_array = np.zeros((len(nodes),)*2, dtype=bool)

    for node in nodes:
        i_node = nodes.index(node)
        connected_nodes = graph[node]

        for connection in connected_nodes:
            i_connect = nodes.index(connection)
            edge_array[i_node, i_connect] = True

    return edge_array, nodes

def remove_connection(graph, from_node, to_node):
    graph[from_node].remove(to_node)
    graph[to_node].remove(from_node)



def make_graph(input_graph):
    graph = nx.Graph()

    nodes = list(input_graph.keys())
    for node in nodes:
        graph.add_node(nodes.index(node))
        for connection in input_graph[node]:
            graph.add_edge(nodes.index(node), nodes.index(connection))

    return graph


if __name__ == "__main__":
    text = common.import_file("input/day25")
    graph = parse_input(text)

    edges, nodes = get_edges(graph)

    # nx_graph = make_graph(graph)
    # nx.draw(nx_graph, with_labels=True)

    remove_connection(graph, nodes[1376], nodes[1368])
    remove_connection(graph, nodes[104], nodes[650])
    remove_connection(graph, nodes[1289], nodes[379])

    # nx_graph = make_graph(graph)
    # nx.draw(nx_graph, with_labels=True)

    block_size = get_block_size(graph)
    common.part(1, block_size * (len(nodes) - block_size))
