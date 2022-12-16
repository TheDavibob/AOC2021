import functools

import numpy as np
import common


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
    for valve in valves.values():
        flow_rate.append(valve["flow_rate"])

    open = [False for valve in valves]

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

    return tuple(flow_rate), tuple(open), tuple(others), tuple(others_dist)


def step(time_remaining, current_position, reduced_valve_dict):
    if time_remaining == 0:
        return 0

    if reduced_valve_dict[current_position]["flow_rate"] == 0:
        value_if_opened = 0
    elif not reduced_valve_dict[current_position]["open"]:
        next_dict = reduced_valve_dict.copy()
        next_dict[current_position]["open"] = True
        value_if_opened = step(
            time_remaining-1,
            current_position,
            next_dict
        ) + (time_remaining - 1) * reduced_valve_dict[current_position]["flow_rate"]
    else:
        value_if_opened = 0

    best_movement = value_if_opened
    for loc, dist in reduced_valve_dict[current_position]["others"].items():
        if dist > time_remaining:
            value_if_move = 0
        else:
            value_if_move = step(
                time_remaining-dist,
                loc,
                reduced_valve_dict
            )
        if value_if_move > best_movement:
            best_movement = value_if_move

    return best_movement


@functools.lru_cache()
def step_2(time_remaining, current_idx, flow_rate, others, others_lengths, prev_idx):
    if time_remaining <= 0:
        return 0

    if flow_rate[current_idx] == 0:
        value_if_opened = 0
    else:
        new_flow = list(flow_rate)
        new_flow[current_idx] = 0
        value_if_opened = step_2(
            time_remaining-1,
            current_idx,
            tuple(new_flow),
            others,
            others_lengths,
            tuple()  # no previous index
        ) + (time_remaining - 1) * flow_rate[current_idx]

    best_movement = value_if_opened
    for new_idx, dist in zip(others[current_idx], others_lengths[current_idx]):
        if new_idx in prev_idx:
            continue  # don't immediately move back

        new_prev_idx = prev_idx + (current_idx,)

        value_if_move = step_2(
            time_remaining-dist,
            new_idx,
            flow_rate,
            others,
            others_lengths,
            new_prev_idx
        )
        if value_if_move > best_movement:
            best_movement = value_if_move

    return best_movement



sample_text="""Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


if __name__ == "__main__":
    # text = common.load_todays_input(__file__)
    text = sample_text
    valves = parse_and_reduce_input(text)
    flow_rates, open_status, links, link_lengths = convert_input(valves)

    # best_movement = step(30, "AA", valves)
    idx_AA = list(valves.keys()).index("AA")
    best_movement = step_2(30, idx_AA, flow_rates, links, link_lengths, tuple())

    common.part(1, best_movement)

    common.part(2, "TBC")
