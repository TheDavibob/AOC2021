from typing import Dict, List

import common


def parse_input(text: str) -> Dict[str, List[str]]:
    # The output is a mapping from each point to all connections
    # that can be reached from that point
    connections = {}
    for line in text.split('\n'):
        if line != "":
            start, end = line.split('-')
            if connections.get(start, None) is None:
                connections[start] = [end]
            else:
                connections[start].append(end)
            if connections.get(end, None) is None:
                connections[end] = [start]
            else:
                connections[end].append(start)

    return connections


def step_path(current_path: List[str], connections: Dict[str, List[str]]):
    # The step in a recursive algorithm

    # How many paths *from this point* reach the end
    count = 0

    current_position = current_path[-1]
    options = connections[current_position]
    for option in options:
        if (option.lower() == option) and (option in current_path):
            # Not a valid option
            continue
        elif option == 'end':
            # This path completes
            count += 1
        else:
            # Go into the option and repeat
            count += step_path(current_path + [option], connections)

    return count


def step_path_2(current_path, connections):
    # How many paths *from this point* reach the end
    count = 0

    current_position = current_path[-1]
    options = connections[current_position]
    for option in options:
        if option == "start":
            continue

        # Add a check if any small cave has already been visited twice
        lower_full = False
        for i, previous_position in enumerate(current_path):
            if (previous_position.lower() == previous_position) and (previous_position in current_path[:i] + current_path[i+1:]):
                lower_full = True
                break

        if lower_full and (option.lower() == option) and (option in current_path):
            # Not a valid option
            continue
        elif option == 'end':
            # Path to end found
            count += 1
        else:
            # Step to next point and count the paths
            count += step_path_2(current_path + [option], connections)

    return count


if __name__ == "__main__":
    text = common.import_file('input/day12_input')
    connections = parse_input(text)
    current_path = ['start']
    print(f"Part 1: {step_path(current_path, connections)}")
    print(f"Part 2: {step_path_2(current_path, connections)}")
