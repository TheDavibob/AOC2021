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


def convert_input(valves):
    flow_rate = []
    for valve in valves.values():
        flow_rate.append(valve["flow_rate"])

    open = [False for valve in valves]

    others = []
    for valve in valves.values():
        idxs = []
        for other in valve["others"]:
            idx = list(valves.keys()).index(other)
            idxs.append(idx)
        others.append(tuple(idxs))

    return tuple(flow_rate), tuple(open), tuple(others)


def step(time_remaining, current_position, valve_dict):
    print(current_position, time_remaining)
    if time_remaining == 0:
        return 0

    if valve_dict[current_position]["flow_rate"] == 0:
        value_if_opened = 0
    elif not valve_dict[current_position]["open"]:
        next_dict = valve_dict.copy()
        next_dict[current_position]["open"] = True
        value_if_opened = step(
            time_remaining-1,
            current_position,
            next_dict
        ) + (time_remaining - 1) * valve_dict[current_position]["flow_rate"]
    else:
        value_if_opened = 0

    best_movement = value_if_opened
    for loc in valve_dict[current_position]["others"]:
        value_if_move = step(
            time_remaining-1,
            loc,
            valve_dict
        )
        if value_if_move > best_movement:
            best_movement = value_if_move

    return best_movement


@functools.lru_cache()
def step_2(time_remaining, current_idx, flow_rate, open, others, prev_idx):
    if time_remaining == 0:
        return 0

    if flow_rate[current_idx] == 0:
        value_if_opened = 0
    elif not open[current_idx]:
        new_open = list(open)
        new_open[current_idx] = True
        value_if_opened = step_2(
            time_remaining-1,
            current_idx,
            flow_rate,
            tuple(new_open),
            others,
            tuple()  # no previous index
        ) + (time_remaining - 1) * flow_rate[current_idx]
    else:
        value_if_opened = 0

    best_movement = value_if_opened
    for new_idx in others[current_idx]:
        if new_idx in prev_idx:
            continue  # don't immediately move back

        new_prev_idx = prev_idx + (current_idx,)

        value_if_move = step_2(
            time_remaining-1,
            new_idx,
            flow_rate,
            open,
            others,
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
    valves = parse_input(text)
    print(valves)
    flow_rates, open_status, links = convert_input(valves)

    # best_movement = step(30, "AA", valves)
    idx_AA = list(valves.keys()).index("AA")
    best_movement = step_2(30, idx_AA, flow_rates, open_status, links, tuple())

    common.part(1, best_movement)

    common.part(2, "TBC")
