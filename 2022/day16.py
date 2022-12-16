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

    return tuple(flow_rate), tuple(others), tuple(others_dist)


def convert_input_simple(valves):
    flow_rate = []
    for valve in valves.values():
        flow_rate.append(valve["flow_rate"])

    others = []
    for valve in valves.values():
        idxs = []
        for other in valve["others"]:
            idx = list(valves.keys()).index(other)
            idxs.append(idx)
        others.append(tuple(idxs))

    return tuple(flow_rate), tuple(others)


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

    if flow_rate[current_idx]*(time_remaining - 1) >= max(flow_rate)*(time_remaining-2):
        return value_if_opened

    best_movement = value_if_opened
    for new_idx, dist in zip(others[current_idx], others_lengths[current_idx]):
        if new_idx in prev_idx:
            continue  # don't immediately move back

        prev_idx = prev_idx + (current_idx,)

        value_if_move = step_2(
            time_remaining-dist,
            new_idx,
            flow_rate,
            others,
            others_lengths,
            prev_idx
        )
        if value_if_move > best_movement:
            best_movement = value_if_move

    return best_movement


@functools.lru_cache()
def step_elephant(time_remaining, current_idx, current_elephant, flow_rate, others, prev_idx, prev_elephant):
    if time_remaining <= 0:
        return 0

    self_movement_options = others[current_idx]
    elephant_movement_options = others[current_elephant]
    if flow_rate[current_idx] == 0:
        self_movement_options = self_movement_options + (current_idx,)

    if flow_rate[current_elephant] == 0:
        if current_elephant != current_idx:
            elephant_movement_options = elephant_movement_options + (current_elephant,)

    max_gain = 0
    for self_movement in self_movement_options:
        if self_movement in prev_idx:
            continue

        for elephant_movement in elephant_movement_options:
            if elephant_movement in prev_elephant:
                continue

            if (elephant_movement == self_movement) and (elephant_movement != current_elephant):
                continue

            increment = 0
            new_flow = list(flow_rate)

            if self_movement == current_idx:
                new_flow[current_idx] = 0
                increment += (time_remaining-1) * flow_rate[current_idx]
                new_prev_idx = tuple()
            else:
                new_prev_idx = prev_idx + (current_idx,)

            if elephant_movement == current_elephant:
                new_flow[current_elephant] = 0
                increment += (time_remaining-1) * flow_rate[current_elephant]
                new_prev_elephant = tuple()
            else:
                new_prev_elephant = prev_elephant + (current_elephant,)

            gain = step_elephant(
                time_remaining-1,
                self_movement,
                elephant_movement,
                tuple(new_flow),
                others,
                new_prev_idx,
                new_prev_elephant
            ) + increment

            if gain > max_gain:
                max_gain = gain

    return max_gain



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


if __name__ == "__main__":
    # text = common.load_todays_input(__file__)
    text = sample_text
    valves = parse_and_reduce_input(text)
    flow_rates, links, link_lengths = convert_input(valves)

    # best_movement = step(30, "AA", valves)
    # idx_AA = list(valves.keys()).index("AA")
    # best_movement = step_2(30, idx_AA, flow_rates, links, link_lengths, tuple())
    # common.part(1, best_movement)

    valves = parse_input(text)
    flow_rates, links = convert_input_simple(valves)
    idx_AA = list(valves.keys()).index("AA")
    max_gain = step_elephant(1, idx_AA, list(valves.keys()).index("BB"), flow_rates, links, tuple(), tuple())
    common.part(2, max_gain)
