from copy import copy

import common


def parse_input(text):
    workflows, part_ratings = text.split("\n\n")

    workflow_map = {}
    for workflow in workflows.split("\n"):
        name, rest = workflow.split("{")
        blocks = rest[:-1].split(",")
        all_conditions = []
        for block in blocks:
            subblocks = block.split(":")
            if len(subblocks) == 1:
                destination = block
                condition = None
            else:
                condition, destination = subblocks
                try:
                    prop, lim = condition.split(">")
                    condition = (prop, ">", int(lim))
                except ValueError:
                    prop, lim = condition.split("<")
                    condition = (prop, "<", int(lim))

            all_conditions.append((condition, destination))

        workflow_map[name] = all_conditions

    parts = []
    for part_rating in part_ratings.split("\n"):
        if part_rating == "":
            continue

        part = {}
        for prop_condition in part_rating[1:-1].split(","):
            prop, value = prop_condition.split("=")
            part[prop] = int(value)

        parts.append(part)

    return workflow_map, parts


def step_part(workflow_map, part):
    part_location = "in"
    while part_location not in ["R", "A"]:
        workflow = workflow_map[part_location]
        for condition, destination in workflow:
            if condition is None:
                part_location = destination
                break

            part_val = part[condition[0]]
            target_val = condition[2]
            if condition[1] == ">":
                if part_val > target_val:
                    part_location = destination
                    break
            if condition[1] == "<":
                if part_val < target_val:
                    part_location = destination
                    break

    return part_location


def step_workflow_range(workflow, parts_map, workflow_map):
    for condition, destination in workflow_map[workflow]:
        parts_in_workflow = parts_map[workflow]
        destination_cubes = []
        origin_cubes = []

        for hypercube in parts_in_workflow:

            if condition is None:
                destination_cubes.append(hypercube)
            elif condition[1] == ">":
                split = split_hypercube(
                    hypercube,
                    condition[0],
                    condition[2]
                )
                destination_cubes.append(split[1])
                origin_cubes.append(split[0])

            elif condition[1] == "<":
                split = split_hypercube(
                    hypercube,
                    condition[0],
                    condition[2]-1
                )
                destination_cubes.append(split[0])
                origin_cubes.append(split[1])
            else:
                raise ValueError(f"condition {condition} not understood")

        if len(origin_cubes) > 0:
            parts_map[workflow] = origin_cubes
        else:
            parts_map.pop(workflow)

        parts_map[destination] = parts_map.get(destination, []) + destination_cubes

    return parts_map


def part_one(workflow_map, parts):
    total = 0
    for part in parts:
        output = step_part(workflow_map, part)
        if output == "A":
            total += get_part_value(part)

    return total


def get_part_value(part):
    value = 0
    for v in part.values():
        value += v

    return value


def part_two(workflow_map):
    parts_map = {"in": [{
        "x": (1, 4000),
        "m": (1, 4000),
        "a": (1, 4000),
        "s": (1, 4000),
    }]}

    while True:
        try:
            next_step = next(key for key in parts_map.keys() if key not in ["A", "R"])
        except StopIteration:
            break
        parts_map = step_workflow_range(next_step, parts_map, workflow_map)

    return parts_map


def get_hypercube_value(hypercube):
    total = 1
    for value in hypercube.values():
        total *= value[1] - value[0] + 1

    return total


def get_all_hypercube_values(hypercubes):
    total = 0
    for hypercube in hypercubes:
        total += get_hypercube_value(hypercube)

    return total

def split_intervals(intervals, split_at):
    # intervals: list of tuples(min, max), assumed ordered
    # split_at is included in the LHS

    lhs = []
    rhs = []
    for left, right in intervals:
        if split_at >= right:
            lhs.append((left, right))
        elif split_at < left:
            rhs.append((left, right))
        else:
            lhs.append((left, split_at))
            rhs.append((split_at+1, right))

    return lhs, rhs


def split_hypercube(hypercube, key, split_at):
    to_split = hypercube[key]
    lhs, rhs = split_intervals([to_split], split_at)
    if len(lhs) == 0:
        left_hand_cube = None
    else:
        left_hand_cube = copy(hypercube)
        left_hand_cube[key] = lhs[0]

    if len(rhs) == 0:
        right_hand_cube = None
    else:
        right_hand_cube = copy(hypercube)
        right_hand_cube[key] = rhs[0]

    return left_hand_cube, right_hand_cube


def merge_intervals(intervals_a, intervals_b):
    all_sorted_intervals = intervals_a + intervals_b
    all_sorted_intervals = sorted(all_sorted_intervals, key=lambda x: x[0])

    n_intervals = len(all_sorted_intervals)
    while True:
        for ((left_0, right_0), (left_1, right_1)) in zip(all_sorted_intervals[:-1],
                                                          all_sorted_intervals[1:]):
            if right_0 > left_1:
                new_interval = (left_0, max(right_0, right_1))
                all_sorted_intervals.remove((left_0, right_0))
                all_sorted_intervals.remove((left_1, right_1))
                all_sorted_intervals.append(new_interval)
                all_sorted_intervals = sorted(all_sorted_intervals, key=lambda x: x[0])
                break

        if len(all_sorted_intervals) == n_intervals:
            break

        n_intervals = len(all_sorted_intervals)

    return all_sorted_intervals



if __name__ == "__main__":
    text = common.import_file("input/day19")

    demo_text = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

    workflow_map, parts = parse_input(text)
    common.part(1, part_one(workflow_map, parts))

    shuffled = part_two(workflow_map)
    common.part(2, get_all_hypercube_values(shuffled["A"]))
