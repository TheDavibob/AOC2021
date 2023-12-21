from __future__ import annotations

import math
from dataclasses import dataclass

import common


@dataclass
class Node:
    name: str
    type: str
    out_connections: list[Node]

    def __repr__(self):
        return "Node " + self.name


@dataclass
class FlipFlopNode(Node):
    state: int  # 0 off, 1 on or 0 low, 1 high

    def __repr__(self):
        return "FlipFlopNode " + self.name


@dataclass
class ConjugationNode(Node):
    in_connections: list[Node]
    state: list[int]

    def __repr__(self):
        return "ConjugationNode " + self.name


@dataclass
class Packet:
    type: int  # 0 or 1
    source: Node
    destination: Node


def parse_input(text):
    nodes: list[Node] = []
    for line in text.split("\n"):
        source, destination = line.split(" -> ")
        if source[0] in ["%", "&"]:
            node_type = source[0]
            name = source[1:]
        else:
            node_type = "b"
            name = source

        destinations = [dest for dest in destination.split(", ")]

        if node_type == "%":
            nodes.append(FlipFlopNode(
                name=name,
                type=node_type,
                out_connections=destinations,
                state=0
            ))
        elif node_type == "&":
            nodes.append(ConjugationNode(
                name=name,
                type=node_type,
                out_connections=destinations,
                in_connections=[],
                state=[]
            ))
        else:
            nodes.append(Node(
                name=name,
                type=node_type,
                out_connections=destinations,
            ))

    for node in nodes:
        node_connections = []
        for connection in node.out_connections:
            try:
                node_connections.append(next(n for n in nodes if n.name == connection))
            except StopIteration:
                new_node = Node(name=connection, type="r", out_connections=[])
                nodes.append(new_node)
                node_connections.append(new_node)

        node.out_connections = node_connections

    for node in nodes:
        for connection in node.out_connections:
            if isinstance(connection, ConjugationNode):
                connection.in_connections.append(node)
                connection.state.append(0)

    return nodes


def receive_packet(node: Node, packet: Packet) -> list[Packet]:
    if node.type == "b":
        raise ValueError("Receiving on broadcast node")
    elif node.type == "r":
        return []
    elif node.type == "%":
        assert isinstance(node, FlipFlopNode)
        if packet.type == 1:
            return []
        else:
            node.state = 1-node.state
            transmit_type = node.state
    elif node.type == "&":
        assert isinstance(node, ConjugationNode)
        source_idx = node.in_connections.index(packet.source)
        node.state[source_idx] = packet.type
        if all(node.state):
            transmit_type = 0
        else:
            transmit_type = 1
    else:
        raise ValueError("Node type not understood")

    packets = []
    for destination in node.out_connections:
        packets.append(Packet(
            source=node,
            destination=destination,
            type=transmit_type)
        )
    return packets


def push_button(nodes: list[Node]):
    n_low_packets = 1  # the button
    n_high_packets = 0
    packet_queue = []

    broadcaster = next(node for node in nodes if node.type == "b")

    try:
        receiver = next(node for node in nodes if node.type == "r")
    except StopIteration:
        receiver = None
    low_received = False
    switch_flicked = None

    for destination in broadcaster.out_connections:
        packet_queue.append(
            Packet(source=broadcaster, destination=destination, type=0)
        )

    while len(packet_queue) > 0:
        next_packet = packet_queue.pop(0)
        new_packets = receive_packet(next_packet.destination, next_packet)
        packet_queue = packet_queue + new_packets
        if next_packet.type == 0:
            n_low_packets += 1
        else:
            n_high_packets += 1

        if (next_packet.destination is receiver) and (next_packet.type == 0):
            low_received = True

        if (next_packet.destination.name == "jm"):
            if any(next_packet.destination.state):
                switch_flicked = next(
                    i for i, s in enumerate(next_packet.destination.state) if s
                )


    return nodes, n_low_packets, n_high_packets, low_received, switch_flicked


def part_one(text):
    nodes = parse_input(text)

    total_low = 0
    total_high = 0

    for _ in range(1000):
        nodes, n_low, n_high, _, _ = push_button(nodes)
        total_low += n_low
        total_high += n_high

    return total_high * total_low


def part_two(text):
    nodes = parse_input(text)

    n_buttons = 0

    low_received = False
    switch_flicking = {i: [] for i in range(4)}

    delta_dict = {i: None for i in range(4)}

    while not low_received:
        nodes, _, _, low_received, switch_flicked = push_button(nodes)
        n_buttons += 1

        if switch_flicked is not None:
            switch_flicking[switch_flicked].append(n_buttons)

            if len(switch_flicking[switch_flicked]) >= 2:
                delta = (
                    switch_flicking[switch_flicked][-1]
                    - switch_flicking[switch_flicked][-2]
                )
            else:
                delta = 0

            if delta > 0:
                delta_dict[switch_flicked] = delta

        if all(delta_dict.values()):
            break

    # This keeps a track of the periodicity of the thing which submits to rx,
    # with rx only triggered when they are all 1.
    print(delta_dict)

    lcm = 1
    for p in delta_dict.values():
        # Again, the problem is set nicely.
        lcm = math.lcm(lcm, p)

    return lcm


if __name__ == "__main__":
    text = common.import_file("input/day20")

    demo_text = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

    demo_text_2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

    assert part_one(demo_text) == 32000000
    assert part_one(demo_text_2) == 11687500
    common.part(1, part_one(text))
    common.part(2, part_two(text))
