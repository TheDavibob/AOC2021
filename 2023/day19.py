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


if __name__ == "__main__":
    text = common.import_file("input/day19")
    workflow_map, parts = parse_input(text)
    common.part(1, part_one(workflow_map, parts))

