import functools

import numpy as np
import common

ROBOT_MAPPING = {
    "ore": 0,
    "clay": 1,
    "obsidian": 2,
    "geode": 3
}


sample_input = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""


def parse_blueprint(blueprint):
    robots = blueprint[:-1].split(": ")[1]
    robots = robots.split(". ")
    rob_map = {}
    for robot in robots:
        name, prices = robot.split(" costs ")
        name = name.split("Each ")[1]
        name = name.split(" robot")[0]

        blocks = prices.split(" and ")
        prices = {}
        for block in blocks:
            cost, type = block.split(" ")
            prices[type] = int(cost)

        rob_map[name] = prices

    return rob_map


def reduce_blueprint(blueprint):
    cost_array = np.zeros((4, 4), dtype=int)
    for robot_name, costs in blueprint.items():
        robot_index = ROBOT_MAPPING[robot_name]
        for to_buy, cost in costs.items():
            cost_index = ROBOT_MAPPING[to_buy]
            cost_array[robot_index, cost_index] = cost

    return cost_array


def evaluate_blueprint(
        n_remaining_steps,
        built_so_far,
        items_so_far,
        cost_array,
        best_at_time,
        best_path
):
    # Process the current minute
    print(best_at_time)

    theoretical = theoretical_max(
        n_remaining_steps,
        built_so_far,
        items_so_far,
        cost_array
    )
    if theoretical <= best_at_time[n_remaining_steps - 1]:
        return 0, best_at_time, []

    new_items = np.zeros(4, dtype=int)
    for idx, (i, b) in enumerate(zip(items_so_far, built_so_far)):
        new_items[idx] = i + b

    if n_remaining_steps == 1:
        return new_items[-1], best_at_time, best_path

    can_build = []
    for rob_idx in range(4):
        cost_line = cost_array[rob_idx]
        if np.all(cost_line <= items_so_far):
            can_build.append(rob_idx)

    can_build = can_build[::-1]

    if (2 not in can_build) or (3 not in can_build):
        new_best_path = best_path + [-1]
        best_n_geodes, best_at_time, final_best_path = evaluate_blueprint(
            n_remaining_steps - 1,
            built_so_far.copy(),
            new_items,
            cost_array,
            best_at_time,
            new_best_path
        )

    else:
        best_n_geodes = 0
        final_best_path = []

    if 3 in can_build:
        can_build = [3]

    for idx in can_build:
        new_built_so_far = built_so_far.copy()
        new_built_so_far[idx] += 1

        items_after_payment = new_items.copy()
        items_after_payment -= cost_array[idx]

        new_best_path = best_path + [idx]
        n_geodes, best_at_time, new_best_path = evaluate_blueprint(
            n_remaining_steps - 1,
            new_built_so_far,
            items_after_payment,
            cost_array,
            best_at_time,
            new_best_path
        )

        if n_geodes > best_n_geodes:
            best_n_geodes = n_geodes
            final_best_path = new_best_path

    if best_n_geodes > best_at_time[n_remaining_steps - 1]:
        best_at_time[n_remaining_steps - 1] = best_n_geodes

    return best_n_geodes, best_at_time, final_best_path


def theoretical_max(n_remaining_steps, built_so_far, items_so_far, cost_array):
    ore_max = theoretical_ore(
        n_remaining_steps,
        built_so_far[0],
        items_so_far[0],
        cost_array[0, 0],
        max(cost_array[:, 0])
    )

    clay_max = theoretical_clay(
        n_remaining_steps,
        built_so_far[1],
        items_so_far[1],
        cost_array[1, 0],
        max(cost_array[:, 1]),
        tuple(ore_max)
    )

    obsidian_max = theoretical_obsidian(
        n_remaining_steps,
        built_so_far[2],
        items_so_far[2],
        cost_array[2, 0],
        cost_array[2, 1],
        max(cost_array[:, 2]),
        tuple(ore_max),
        tuple(clay_max)
    )

    geode_max = theoretical_geode(
        n_remaining_steps,
        built_so_far[3],
        items_so_far[3],
        cost_array[3, 0],
        cost_array[3, 2],
        tuple(ore_max),
        tuple(obsidian_max)
    )

    return geode_max[-1]


@functools.cache
def theoretical_ore(
        n_remaining_steps,
        ore_mines,
        ore_so_far,
        ore_cost_in_ore,
        max_number_ore_mines
):
    ore = ore_so_far * np.ones(n_remaining_steps, dtype=int)
    n_added = 0
    for idx in range(n_remaining_steps):
        ore[idx] += (n_added + ore_mines) + ore[idx-1]

        if n_added + ore_mines == max_number_ore_mines:
            pass
        elif ore[idx-1] - n_added*ore_cost_in_ore >= ore_cost_in_ore:
            n_added += 1

    return ore


@functools.cache
def theoretical_clay(
        n_remaining_steps,
        clay_mines,
        clay_so_far,
        clay_cost_in_ore,
        max_number_clay_mines,
        max_ore_at_time
):
    clay = clay_so_far * np.ones(n_remaining_steps, dtype=int)
    n_added = 0
    for idx in range(n_remaining_steps):
        clay[idx] += (n_added + clay_mines) + clay[idx-1]

        if n_added + clay_mines == max_number_clay_mines:
            pass
        elif max_ore_at_time[idx] - n_added*clay_cost_in_ore >= clay_cost_in_ore:
            n_added += 1

    return clay


@functools.cache
def theoretical_obsidian(
        n_remaining_steps,
        obsidian_mines,
        obsidian_so_far,
        obsidian_cost_in_ore,
        obsidian_cost_in_clay,
        max_number_obsidian_mines,
        max_ore_at_time,
        max_clay_at_time
):
    obsidian = obsidian_so_far * np.ones(n_remaining_steps, dtype=int)
    n_added = 0
    for idx in range(n_remaining_steps):
        obsidian[idx] += (n_added + obsidian_mines) + obsidian[idx-1]

        if n_added + obsidian_mines == max_number_obsidian_mines:
            continue
        elif (
            max_ore_at_time[idx] - n_added*obsidian_cost_in_ore >= obsidian_cost_in_ore
        ) and (
            max_clay_at_time[idx] - n_added*obsidian_cost_in_clay >= obsidian_cost_in_clay
        ):
            n_added += 1

    return obsidian


@functools.cache
def theoretical_geode(
        n_remaining_steps,
        geode_mines,
        geode_so_far,
        geode_cost_in_ore,
        geode_cost_in_obsidian,
        max_ore_at_time,
        max_obsidian_at_time
):
    geode = geode_so_far * np.ones(n_remaining_steps, dtype=int)
    n_added = 0
    for idx in range(n_remaining_steps):
        geode[idx] += (n_added + geode_mines) + geode[idx - 1]

        if (
            max_ore_at_time[idx] - n_added*geode_cost_in_ore >= geode_cost_in_ore
        ) and (
            max_obsidian_at_time[idx] - n_added*geode_cost_in_obsidian >= geode_cost_in_obsidian
        ):
            n_added += 1

    return geode


@functools.cache
def evaluate_blueprint_2(
        n_remaining_time,
        built_so_far,
        items_so_far,
        cost_array,
        max_costs,
        greedy=False,
):
    best_geodes = 0

    built_so_far = np.array(built_so_far)
    items_so_far = np.array(items_so_far)

    for build_next in range(3, -1, -1):
        if (build_next != 3) \
                and (max_costs[build_next] <= built_so_far[build_next]):
            continue

        build_cost = np.array(cost_array[build_next])
        if np.any(build_cost[built_so_far == 0]):
            continue

        remaining_materials = build_cost - items_so_far
        time_to_build = 1
        while np.any(remaining_materials > 0):
            remaining_materials -= built_so_far
            time_to_build += 1

        if n_remaining_time - time_to_build <= 0:
            items = items_so_far + n_remaining_time * built_so_far
            n_geodes = items[-1]
        else:
            n_geodes = evaluate_blueprint_2(
                n_remaining_time - time_to_build,
                tuple(built_so_far + np.eye(4, dtype=int)[build_next]),
                tuple(items_so_far + built_so_far * time_to_build - build_cost),
                cost_array,
                max_costs,
                greedy=greedy
            )

        if n_geodes > best_geodes:
            best_geodes = n_geodes

        if greedy:
            return best_geodes

    return best_geodes


if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    blueprints = []
    for line in sample_input.split("\n"):
        if line == "":
            continue
        else:
            blueprints.append(reduce_blueprint(parse_blueprint(line)))

    cumulative = 0
    start = (1, 0, 0, 0)
    for i, blueprint in enumerate(blueprints):
        print(f"Blueprint {i+1}")
        max_costs = tuple(
            max(blueprint[:, i]) for i in range(4)
        )
        cost_array = tuple(
            tuple(b) for b in blueprint
        )

        max_geodes = evaluate_blueprint_2(
            24,
            start,
            (0, 0, 0, 0),
            cost_array,
            max_costs
        )
        print(max_geodes)
        cumulative += (i+1) * max_geodes

    common.part(1, cumulative)

    cumulative = 1
    start = (1, 0, 0, 0)
    for i, blueprint in enumerate(blueprints[:3]):
        print(f"Blueprint {i+1}")
        max_costs = tuple(
            max(blueprint[:, i]) for i in range(4)
        )
        cost_array = tuple(
            tuple(b) for b in blueprint
        )

        max_geodes = evaluate_blueprint_2(
            32,
            start,
            (0, 0, 0, 0),
            cost_array,
            max_costs,
            greedy=False
        )
        print(max_geodes)
        cumulative *= max_geodes

    common.part(2, cumulative)
