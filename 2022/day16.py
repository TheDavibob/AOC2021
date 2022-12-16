import functools
from copy import copy

import numpy as np

import common


sample_text = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


def parse_input(text):
    valve_dict = {}
    for line in text.split("\n"):
        if line == "":
            continue

        valve_name = line[6:8]

        flow_rate = line.split("=")[1]
        flow_rate = int(flow_rate.split(";")[0])

        try:
            others = line.split("valves ")[1]
            others = tuple([x for x in others.split(", ")])
        except IndexError:
            others = (line.split("valve ")[-1],)

        valve_dict[valve_name] = {
            "open": False,
            "flow_rate": flow_rate,
            "others": others
        }

    return valve_dict


def parse_and_reduce_input(text):
    valve_dict = {}
    for line in text.split("\n"):
        if line == "":
            continue

        valve_name = line[6:8]

        flow_rate = line.split("=")[1]
        flow_rate = int(flow_rate.split(";")[0])

        try:
            others = line.split("valves ")[1]
            others = tuple([x for x in others.split(", ")])
        except IndexError:
            others = (line.split("valve ")[-1],)

        valve_dict[valve_name] = {
            "flow_rate": flow_rate,
            "others": {other: 1 for other in others}
        }

    is_reduced = True
    while is_reduced:
        is_reduced = False
        for valve_name, valve_info in valve_dict.items():
            if valve_name == "AA":
                continue

            if valve_info["flow_rate"] == 0:
                link = valve_info["others"]
                dist = sum(link.values())
                to_from = list(link.keys())
                valve_dict[to_from[0]]["others"][to_from[1]] = dist
                valve_dict[to_from[0]]["others"].pop(valve_name)

                valve_dict[to_from[1]]["others"][to_from[0]] = dist
                valve_dict[to_from[1]]["others"].pop(valve_name)

                valve_dict.pop(valve_name)
                is_reduced = True
                break

    for valve in valve_dict.values():
        valve["open"] = False

    return valve_dict


def convert_input(valves):
    flow_rate = []
    names = []
    for name, valve in valves.items():
        names.append(name)
        flow_rate.append(valve["flow_rate"])

    others = []
    others_dist = []
    for valve in valves.values():
        idxs = []
        dists = []
        for other, dist in valve["others"].items():
            idx = list(valves.keys()).index(other)
            idxs.append(idx)
            dists.append(dist)
        others.append(tuple(idxs))
        others_dist.append(tuple(dists))

    return tuple(flow_rate), tuple(names), tuple(others), tuple(others_dist)


def point_to_point_distances(links, link_lengths):
    p2p_distance = np.zeros((len(links),)*2, dtype=int)
    for i, link in enumerate(links):
        for to, length in zip(link, link_lengths[i]):
            p2p_distance[i, to] = length

    changed = True
    while changed:
        changed = False
        for i in range(p2p_distance.shape[0]):
            for j in range(p2p_distance.shape[1]):
                if i == j:
                    continue

                for k in range(p2p_distance.shape[0]):
                    if (p2p_distance[i, k] > 0) and (p2p_distance[k, j] > 0):
                        distance = p2p_distance[i, k] + p2p_distance[k, j]
                        if (p2p_distance[i, j] == 0) or (distance < p2p_distance[i, j]):
                            p2p_distance[i, j] = distance
                            changed = True

    return p2p_distance


def get_all_sequences(p2p_distances, seen_so_far, max_length, current_length):
    n_nodes = p2p_distances.shape[0]
    current_point = seen_so_far[-1]
    not_seen = [x for x in range(n_nodes) if x not in seen_so_far]
    new_sequences = [seen_so_far]
    for new in not_seen:
        new_length = current_length + p2p_distances[current_point, new]
        if new_length <= max_length:
            new_sequences = new_sequences + get_all_sequences(
                p2p_distances,
                seen_so_far + [new],
                max_length,
                new_length
            )

    return new_sequences


def get_sequence_value(sequence, p2p_distances, flow_rates, max_time):
    sum_flow = 0
    time = 0
    for fro, to in zip(sequence[:-1], sequence[1:]):
        time += p2p_distances[fro, to] + 1
        rem_time = max_time - time
        sum_flow += rem_time * flow_rates[to]
        # print(time, sum_flow)

    return sum_flow


def double_value(sequence_0, sequence_1, p2p_distances, flow_rates, max_time):
    sum_flow = 0
    time = 0
    idx_0 = 0
    time_0 = 0
    idx_1 = 0
    time_1 = 0

    while time < max_time:
        if time_0 == time:
            if idx_0 + 1 == len(sequence_0):
                time_0 = max_time
            else:
                time_0 += p2p_distances[sequence_0[idx_0], sequence_0[idx_0+1]]
                idx_0 = idx_0 + 1
                time_0 += 1
                if sequence_0[idx_0] not in sequence_1[:idx_1+1]:
                    rem_time = max_time - time_0
                    sum_flow += rem_time * flow_rates[sequence_0[idx_0]]
                    # print(f"@self {sequence_0[idx_0]} {time_0}: {sum_flow}")

        if time_1 == time:
            if idx_1 + 1 == len(sequence_1):
                time_1 = max_time
            else:
                time_1 += p2p_distances[sequence_1[idx_1], sequence_1[idx_1+1]]
                idx_1 = idx_1 + 1
                time_1 += 1
                if sequence_1[idx_1] not in sequence_0[:idx_0+1]:
                    rem_time = max_time - time_1
                    sum_flow += rem_time * flow_rates[sequence_1[idx_1]]
                    # print(f"@elephant {sequence_1[idx_1]} {time_1}: {sum_flow}")

        time += 1

    return sum_flow


if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    valves = parse_and_reduce_input(text)
    flow_rates, names, links, link_lengths = convert_input(valves)

    p2p = point_to_point_distances(links, link_lengths)
    idx_AA = list(valves.keys()).index("AA")
    sequences = get_all_sequences(p2p, [idx_AA], 30, 0)

    max_flow = 0
    for sequence in sequences:
        sum_flow = get_sequence_value(sequence, p2p, flow_rates, 30)
        if sum_flow > max_flow:
            max_flow = sum_flow

    common.part(1, max_flow)

    sequences = get_all_sequences(p2p, [idx_AA], 26, 0)
    base_seq = []
    for sequence in sequences:
        base_seq.append(get_sequence_value(sequence, p2p, flow_rates, 26))

    sorted_sequences = [x for y, x in sorted(zip(base_seq, sequences))][::-1]
    sorted_base = [y for y, x in sorted(zip(base_seq, sequences))][::-1]

    max_flow_2 = 0
    for i, sequence_0 in enumerate(sorted_sequences):
        for j, sequence_1 in enumerate(sorted_sequences):
            if sorted_base[i] + sorted_base[j] < max_flow_2:
                break

            sum_flow = double_value(sequence_0, sequence_1, p2p, flow_rates, 26)
            if sum_flow > max_flow_2:
                max_flow_2 = sum_flow

    common.part(2, max_flow_2)
