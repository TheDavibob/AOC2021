from copy import copy
from typing import NamedTuple, List

import networkx

import common


def create_dependency_map(text):
    dependency_map = {}
    for line in text.split('\n'):
        if line == "":
            continue
        required, result = line.split(' => ')
        num_prod, product = result.split(' ')
        requsits = []
        for req in required.split(', '):
            num, r = req.split(' ')
            requsits.append((r, int(num)))

        dependency_map[(product, int(num_prod))] = requsits

    return dependency_map


def create_dependency_graph(dependency_map):
    g = networkx.DiGraph()
    g.add_node("ORE")
    for k, v in dependency_map.items():
        g.add_node(k[0])

    for k, v in dependency_map.items():
        for source in v:
            g.add_edge(source[0], k[0])

    return g


class Edge(NamedTuple):
    input: str
    output: str
    required: int
    makes: int


def create_all_edges(dependency_map):
    edges = []
    for k, v in dependency_map.items():
        for source in v:
            edges.append(Edge(
                source[0],
                k[0],
                source[1],
                k[1]
            ))

    return edges


def reduce_graph(edges: List[Edge], target="FUEL"):
    pipe_to_fuel = {e.input for e in edges if e.output == target}
    pipe_only_to_fuel = {p for p in pipe_to_fuel if p not in {e.input for e in edges if e.output != target}}

    # We now have a list of things that fuel depends on, which nothing else depends on
    for link_to_remove in pipe_only_to_fuel:
        edge_to_remove = [e for e in edges if e.input == link_to_remove][0]
        edges.remove(edge_to_remove)
        required = edge_to_remove.required
        input_edges = [e for e in edges if e.output == link_to_remove]
        for input_edge in input_edges:
            edges.remove(input_edge)
            new_required = calc_required_input(required, input_edge.required, input_edge.makes)

            existing_matching_edge = [e for e in edges if (e.input == input_edge.input) and (e.output == target)]
            if existing_matching_edge:
                new_required = existing_matching_edge[0].required + new_required
                edges.remove(existing_matching_edge[0])

            edges.append(Edge(
                input_edge.input,
                target,
                new_required,
                1
            ))


def calc_required_input(output_required, input_required, input_makes):
    if output_required % input_makes == 0:
        num_input_required = input_required * (output_required // input_makes)
    else:
        num_input_required = input_required * ((output_required // input_makes) + 1)
    return num_input_required


def reduce_all(edges):
    while len(edges) > 1:
        reduce_graph(edges)

    return edges[0].required


def reduce_with_more_fuel(edges, n):

    input_edges = copy(edges)
    input_edges.append(Edge(
        'FUEL',
        'SUPERFUEL',
        n,
        1
    ))
    while len(input_edges) > 1:
        reduce_graph(input_edges, 'SUPERFUEL')

    output = input_edges[0].required

    return output


def optimise_n(edges):
    i = 0
    guess = 1
    while True:
        guess = 10**i
        if reduce_with_more_fuel(edges, guess) - 1000000000000 > 0:
            break
        i+=1

    max_value = guess
    min_value = 0

    while max_value > min_value + 1:
        guess = min_value + (max_value - min_value) // 2
        output = reduce_with_more_fuel(edges, guess) - 1000000000000
        if output > 0:
            # guess is too big
            max_value = guess
        else:
            # guess is too small
            min_value = guess

    return min_value



if __name__ == "__main__":
    text = common.import_file("../input/day14")
    dependency_map = create_dependency_map(text)
    edges = create_all_edges(dependency_map)

    common.part(1, reduce_all(edges))

    edges = create_all_edges(dependency_map)
    common.part(2, optimise_n(edges))