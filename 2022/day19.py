import numpy as np
import common

ROBOT_MAPPING = {
    "ore": 0,
    "clay": 1,
    "obsidian": 2,
    "geode": 3
}


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
    new_items = np.zeros(4, dtype=int)
    for idx, (i, b) in enumerate(zip(items_so_far, built_so_far)):
        new_items[idx] = i + b

    if n_remaining_steps == 1:
        return new_items[-1]

    can_build = []
    for rob_idx in range(4):
        cost_line = cost_array[rob_idx]
        if np.all(cost_line <= new_items):
            can_build.append(rob_idx)

    if (2 not in can_build) or (3 not in can_build):
        best_n_geodes = evaluate_blueprint(
            n_remaining_steps - 1,
            built_so_far.copy(),
            new_items,
            cost_array
        )

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
    for line in text.split("\n"):
        if line == "":
            continue
        else:
            blueprints.append(reduce_blueprint(parse_blueprint(line)))

    start = np.zeros(4,)
    start[0] = 1
    n_geodes = evaluate_blueprint(24, start, np.zeros(4, ), blueprints[0])

    common.part(1, "TBC")

    common.part(2, "TBC")
