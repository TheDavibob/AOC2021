import functools
from copy import copy

import numpy as np
from tqdm import tqdm

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
def count_paths(
        time_remaining,
        current_idx,
        flow_rate,
        others,
        others_lengths,
        prev_idx
):
    if time_remaining <= 0:
        return 0

    n_paths = 0

    if flow_rate[current_idx] != 0:
        new_flow_rate = list(flow_rate)
        new_flow_rate[current_idx] = 0
        n_paths += count_paths(
            time_remaining-1,
            current_idx,
            tuple(new_flow_rate),
            others,
            others_lengths,
            tuple()
        )

    for new_idx, dist in zip(others[current_idx], others_lengths[current_idx]):
        if new_idx in prev_idx:
            continue  # don't immediately move back

        prev_idx = prev_idx + (current_idx,)

        n_paths += count_paths(
            time_remaining-dist,
            new_idx,
            flow_rate,
            others,
            others_lengths,
            prev_idx
        )

    return n_paths


@functools.lru_cache()
def step_elephant(time_remaining, current_idx, current_elephant, flow_rate, others,
                  prev_idx, prev_elephant):
    if time_remaining <= 0:
        return 0

    self_movement_options = others[current_idx]
    elephant_movement_options = others[current_elephant]
    if flow_rate[current_idx] != 0:
        self_movement_options = self_movement_options + (current_idx,)

    if flow_rate[current_elephant] != 0:
        if current_elephant != current_idx:
            elephant_movement_options = elephant_movement_options + (current_elephant,)

    if flow_rate[current_idx]*(time_remaining - 1) \
            >= max(flow_rate)*(time_remaining-2):
        if current_idx in self_movement_options:
            self_movement_options = (current_idx,)

    if flow_rate[current_elephant]*(time_remaining - 1) \
            >= max(flow_rate)*(time_remaining-2):
        if current_elephant in elephant_movement_options:
            elephant_movement_options = (current_elephant,)

    self_movement_options = tuple(
        sorted(self_movement_options, key=lambda x: flow_rate[x])[::-1]
    )
    elephant_movement_options = tuple(
        sorted(elephant_movement_options, key=lambda x: flow_rate[x])[::-1]
    )

    max_gain = 0
    for self_movement in self_movement_options:
        if self_movement in prev_idx:
            continue

        for elephant_movement in elephant_movement_options:
            if elephant_movement in prev_elephant:
                continue

            if (elephant_movement == self_movement) and (elephant_movement != current_elephant):
                continue

            if (elephant_movement == self_movement) and (self_movement != current_idx):
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

            if elephant_movement < self_movement:
                self_movement, elephant_movement = elephant_movement, self_movement
                new_prev_idx, new_prev_elephant = new_prev_elephant, new_prev_idx

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

            if sum(new_flow) * time_remaining - 1 < max_gain:
                return max_gain

    print(time_remaining, max_gain)

    return max_gain


def breadth_first(
        current_time,
        current_positions,
        current_scores,
        current_active_valves,
        flow_rates,
        links
):
    new_time = current_time - 1

    # Should we allow "no move"?
    new_positions = copy(current_positions)
    new_scores = copy(current_scores)
    new_active_valves = copy(current_active_valves)
    # new_positions = []
    # new_scores = []
    # new_active_valves = []

    for pos, score, valves in zip(
            current_positions, current_scores, current_active_valves
    ):
        new_score = score + sum(flow_rates[v] for v in valves)
        idx_self, idx_el = pos

        opt_self = links[idx_self]
        opt_el = links[idx_el]

        if (flow_rates[idx_self] != 0) and (idx_self not in valves):
            opt_self = opt_self + (idx_self,)

        if (flow_rates[idx_el] != 0) and (idx_el not in valves):
            if idx_el != idx_self:
                opt_el = opt_el + (idx_el,)

        opt_self = tuple(
            sorted(opt_self, key=lambda x: flow_rates[x])[::-1]
        )
        opt_el = tuple(
            sorted(opt_el, key=lambda x: flow_rates[x])[::-1]
        )

        for move_self in opt_self:
            for move_el in opt_el:
                new_valves = copy(valves)
                new_position = tuple(sorted((move_self, move_el)))
                if move_el == idx_el:
                    new_valves.add(idx_el)
                if move_self == idx_self:
                    new_valves.add(idx_self)

                replaced = False
                if new_position in new_positions:
                    # Can we improve any estimates?
                    locs = [i for i, x in enumerate(new_positions) if x == new_position]
                    for loc in locs:
                        if new_valves == new_active_valves[loc]:
                            if new_score >= new_scores[loc]:
                                new_scores[loc] = new_score
                                replaced = True
                                break
                            else:
                                replaced = True
                                break

                        if new_valves.issubset(new_active_valves[loc]):
                            if new_score < new_scores[loc]:
                                # Discard - the existing is better
                                replaced = True
                                break

                if not replaced:
                    new_positions.append(new_position)
                    new_scores.append(new_score)
                    new_active_valves.append(new_valves)

    unique_positions = set(new_positions)
    new_new_positions = []
    new_new_scores = []
    new_new_active_valves = []
    for unique_position in unique_positions:
        locs_pos = [i for i, x in enumerate(new_positions) if x == unique_position]
        unique_position_valves = (new_active_valves[loc] for loc in locs_pos)
        for unique_position_valve in unique_position_valves:
            unique_score = max([
                z for x, y, z in zip(new_positions, new_active_valves, new_scores)
                if (x == unique_position) and (y == unique_position_valve)
            ])

            new_new_positions.append(unique_position)
            new_new_active_valves.append(set(unique_position_valve))
            new_new_scores.append(unique_score)

    return new_time, new_new_positions, new_new_scores, new_new_active_valves


def array_version(flow_rates, links):
    n_non_zero_flows = sum(flow_rates > 0)
    all_state_array = np.zeros(
        (len(flow_rates), len(flow_rates), n_non_zero_flows),
        dtype=int
    )


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
    text = common.load_todays_input(__file__)
    valves = parse_and_reduce_input(text)
    flow_rates, links, link_lengths = convert_input(valves)

    # best_movement = step(30, "AA", valves)
    idx_AA = list(valves.keys()).index("AA")
    # best_movement = step_2(30, idx_AA, flow_rates, links, link_lengths, tuple())
    # common.part(1, best_movement)

    # valves = parse_input(text)
    # flow_rates, links = convert_input_simple(valves)
    # idx_AA = list(valves.keys()).index("AA")
    # time = 26
    # pos = [(idx_AA, idx_AA)]
    # scores = [0]
    # active = [set()]

    # for _ in range(26):
    #     time, pos, scores, active = \
    #         breadth_first(time, pos, scores, active, flow_rates, links)
    #     print(time, len(pos))

    common.part(2, count_paths(
        26,
        idx_AA,
        flow_rates,
        links,
        link_lengths,
        tuple()
    ))
