from copy import deepcopy


def parse_input(text):
    starts, gates = text.split("\n\n")
    vals_dict = {}
    for line in starts.split("\n"):
        var, val = line.split(": ")
        vals_dict[var] = int(val)

    gates_list = []
    for line in gates.split("\n"):
        if line == "":
            continue

        left, right = line.split(" -> ")
        op0, operand, op1 = left.split(" ")
        gates_list.append(((op0, op1), operand, right))

    return vals_dict, gates_list


def step(values, gates):
    unused_gates = []
    for gate in gates:
        operands, operation, target = gate
        if operands[0] in values and operands[1] in values:
            o0 = values[operands[0]]
            o1 = values[operands[1]]
            if operation == "AND":
                values[target] = o0 & o1
            elif operation == "OR":
                values[target] = o0 | o1
            elif operation == "XOR":
                values[target] = o0 ^ o1
            else:
                raise ValueError(f"Operation {operation} not understood")
        else:
            unused_gates.append(gate)

    return values, unused_gates


def reassemble_z(values):
    total = 0
    bit = 0
    while True:
        try:
            total += (1 << bit) * values[f"z{bit:02d}"]
            bit += 1
        except KeyError:
            break

    return total


def run_on_any_input(x, y, gates, ref_values):
    values = {}
    i = 0
    while True:
        if f"x{i:02d}" in ref_values:
            values[f"x{i:02d}"] = 0
            i += 1
        else:
            break

    i = 0
    while True:
        if f"y{i:02d}" in ref_values:
            values[f"y{i:02d}"] = 0
            i += 1
        else:
            break

    for i, b in enumerate(bin(x)[:2:-1]):
        values[f"x{i:02d}"] = int(b=="1")

    for i, b in enumerate(bin(y)[:2:-1]):
        values[f"y{i:02d}"] = (b=="1")

    return run(values, gates)


def run(values, gates):
    while len(gates) > 0:
        values, gates = step(values, gates)

    return reassemble_z(values)


if __name__ == "__main__":
    with open("input/day24") as file:
        text = file.read()

    values, gates = parse_input(text)
    ref_values = deepcopy(values)
    ref_gates = deepcopy(gates)
    while len(gates) > 0:
        values, gates = step(values, gates)

    print(f"Part 1: {reassemble_z(values)}")

    z = run_on_any_input(0, 0, ref_gates, ref_values)