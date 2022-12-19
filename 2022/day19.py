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


def evaluate_blueprint(n_remaining_steps, built_so_far, items_so_far, cost_array):
    # Process the current minute
    print(n_remaining_steps, built_so_far, items_so_far)

    new_items = np.zeros(4, dtype=int)
    for idx, (i, b) in enumerate(zip(items_so_far, built_so_far)):
        new_items[idx] = i + b

    if n_remaining_steps == 1:
        return new_items[-1]

    if n_remaining_steps ** 2 + items_so_far[2] < cost_array[3, 2]:
        # We cannot get enough obsidian to build a new geode thing
        # FIX THIS - is a good heuristic

        # Idea: compute the maximum possible of each item that could
        # be mined, if a new extractor was built every sample
        # If say, cannot mine enough obsidian to make any geodes,
        # just compute the final answer (i.e. geode mines * rem time + geodes)
        # If say, cannot mine enough clay to make any more obsidian,
        # trim the obsidian max (to obsidian mines * rem_time + obsidian) and repeat.
        # Feasibly could do same for clay, but this gets messy.
        return new_items[-1]

    can_build = []
    for rob_idx in range(4):
        cost_line = cost_array[rob_idx]
        if np.all(cost_line <= items_so_far):
            can_build.append(rob_idx)

    can_build = can_build[::-1]

    if (2 not in can_build) or (3 not in can_build):
        best_n_geodes = evaluate_blueprint(
            n_remaining_steps - 1,
            built_so_far.copy(),
            new_items,
            cost_array
        )
    else:
        best_n_geodes = 0

    if 3 in can_build:
        can_build = [3]

    for idx in can_build:
        new_built_so_far = built_so_far.copy()
        new_built_so_far[idx] += 1
        n_geodes = evaluate_blueprint(
            n_remaining_steps - 1,
            new_built_so_far,
            new_items,
            cost_array
        )

        if n_geodes > best_n_geodes:
            best_n_geodes = n_geodes

    return best_n_geodes



if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    blueprints = []
    for line in sample_input.split("\n"):
        if line == "":
            continue
        else:
            blueprints.append(reduce_blueprint(parse_blueprint(line)))

    start = np.zeros(4,)
    start[0] = 1
    n_geodes = evaluate_blueprint(24, start, np.zeros(4, ), blueprints[0])

    common.part(1, "TBC")

    common.part(2, "TBC")
