import functools
from copy import deepcopy

from tqdm import tqdm


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

    for i, b in enumerate(bin(x)[:1:-1]):
        values[f"x{i:02d}"] = int(b=="1")

    for i, b in enumerate(bin(y)[:1:-1]):
        values[f"y{i:02d}"] = (b=="1")

    return run(values, gates)


def run(values, gates):
    i_iterations = 0
    while len(gates) > 0:
        values, gates = step(values, gates)
        i_iterations += 1
        if i_iterations >= 100:
            raise ValueError("Borked")

    return reassemble_z(values)


def try_swap(swap, initial_gates, x, y):
    new_gates = []
    for gate in initial_gates:
        target = gate[-1]
        if target not in swap:
            pass
        elif target == swap[0]:
            target = swap[1]
        elif target == swap[1]:
            target = swap[0]

        new_gates.append(gate[:-1] + (target,))

    z = run_on_any_input(x, y, new_gates, ref_values)
    return z == x + y


@functools.cache
def get_all_requirements(target, gates):
    requirements = [target]
    entry_gates = [g for g in gates if g[-1] == target]
    if len(entry_gates) == 0:
        return requirements

    entry_points = entry_gates[0][0]
    requirements.extend(get_all_requirements(entry_points[0], gates))
    requirements.extend(get_all_requirements(entry_points[1], gates))
    requirements = sorted(list(set(requirements)))
    return requirements


if __name__ == "__main__":
    with open("input/day24") as file:
        text = file.read()

    values, gates = parse_input(text)
    ref_values = deepcopy(values)
    ref_gates = tuple(deepcopy(gates))

    print(f"Part 1: {run(values, gates)}")

    z = run_on_any_input(0, 1, ref_gates, ref_values)

    # We have:
    # 46 exit gates
    # 90 layer 1 nodes
    # Node by node:
    # To z00 is correct: just x00 ^ y00
    # z01 = prt ^ jnj
    #   prt = x00 & y00 # good
    #   jnj = x01 ^ y01 # good
    # Note: we should really be able to build things up like this, which is a good thing to notice.
    # z02 = wsm ^ qnf
    #   wsm = y02 ^ x02
    #   qnf = kmf | cdb
    #       kmf = x01 & y01
    #       cdb = jnj & prt
    # Still going strong
    # z03 = vnm ^ mgr
    #   vnm = jrf | shr
    #       jrf = x02 & y02
    #       shr = wsm & qnf
    #   mgr = x03 & y03
    # So there's an algorithm here: nah they're all pretty good.


    # OK: They're all the same:
    # zj = a ^ b
    #   wlog a = xj ^ yj - some slips here: already solves three of the issues!
    #   x21 & y21 -> rqf is wrong   # SWAP rqf, nnr
    #   y44 & x44 -> qqr is also wrong, and it's off by 1 too (it's for z45)
    #       qqr and bmv should be swapped, not sure what that leaves though. Maybe not - this is the last index
    #   y16 & x16 -> bss is wrong   # SWAP bss, grr


    # z37 doesn't get a proper map: what's going on?
    # The XOR goes to gcg, which is (badly?) XORred to rrn
    #

    # On the other thread:
    #   bmv & fjs -> kwh when it should be |
    #   kcm & grr -> tnn when it should be |
    #   kcm ^ grr -> fkb when it should be |
    # The previous swaps don't help here
    # There is no kcm | grr anywhere, which suggests it shouldn't be used for this op
    # Ah wait, possibly the & ^ is an overcomplicated way of doing this
    # Again, no obvious | on the bmv/fjs pair, might be something weird.

    swaps = [("rqf", "nnr"), ("bss", "grr"), ("rrn", "z37")]
    new_gates = []
    for gate in ref_gates:
        target = gate[-1]
        for swap in swaps:
            if target == swap[0]:
                target = swap[1]
            elif target == swap[1]:
                target = swap[0]

        new_gates.append(gate[:-1] + (target,))

    outputs = [g[-1] for g in ref_gates]
    potential_swaps = [(o, p) for o in outputs for p in outputs if o > p]
    potential_swaps_2 = []
    # for swap in tqdm(potential_swaps):
    #     try:
    #         works = try_swap(swap, new_gates, 0, 0)
    #         if not works:
    #             continue
    #         works &= try_swap(swap, new_gates, 2**22-1, 2**22-1)
    #         if not works:
    #             continue
    #         works &= try_swap(swap, new_gates, 10000000, 1000000)
    #         if not works:
    #             continue
    #         works &= try_swap(swap, new_gates, 512, 1212612612)
    #         if not works:
    #             continue
    #     except ValueError:
    #         works = False
    #     if works:
    #         potential_swaps_2.append(swap)

    and_gates = [g for g in ref_gates if g[1] == "AND"]
    or_gates = [g for g in ref_gates if g[1] == "OR"]
    xor_gates = [g for g in ref_gates if g[1] == "XOR"]

    # SWAPS:
    # The gate which feeds to z16, z31, z37 aren't correct: should all be XORs
    first_and_targets = [g[-1] for g in and_gates if g[0][0][0] in ["x", "y"]]
    follow_up = [g for g in gates if g[0][0] in first_and_targets or g[0][1] in first_and_targets]
    wrong = [g for g in follow_up if g[1] != "OR"]

    into_z = [g for g in ref_gates if g[-1][0] == "z"]
    dodgy = [g for g in into_z if g[1] != "XOR"]
    # z37 needs to swap with whatever y37 & x37 should be
    # z16 needs to swap with whatever tnn | bss should be
    # z31 needs to swap with whatever qsj & tjk should be
    # [("rqf", "nnr"), ("bss", "grr"), ("rrn", "z37")]
    # rqf is currently the output of y21 & x21, which feeds to z21. Either rqf should swap or the next level should
    # Swapping z16 will probably deal with the bss issue
    # rqf is still wrong, so rqf <-> nnr is probably still right
    # fkb is definitely wrong -- needs to come from an OR
    # z31 is wrong
    # z37 is wrong: swap with gcg - doesn't work
    # Dangling XOR gates:  # Should all ppipe into a z
    #   kcm ^ grr -> fkb
    #   gcg ^ nbm -> rrn
    #   qsj ^ tjk -> rdn
    for g in into_z:
        print(
            g[-1],
            "\t",
            g,
            "\t",
            [h for h in ref_gates if h[-1] in g[0] and h[0][0][0] in ("x", "y")],
            "\t",
            [h for h in ref_gates if h[-1] in g[0] and h[0][0][0] not in ("x", "y")]
        )
    swaps = [("rqf", "nnr"), ("fkb", "z16"), ("rrn", "z37"), ("rdn", "z31")]
    new_gates = []
    for gate in ref_gates:
        target = gate[-1]
        for swap in swaps:
            if target == swap[0]:
                target = swap[1]
            elif target == swap[1]:
                target = swap[0]

        new_gates.append(gate[:-1] + (target,))

    print("POST SWAPS")
    print("------")
    into_z = [g for g in new_gates if g[-1][0] == "z"]
    for g in into_z:
        print(
            g[-1],
            "\t",
            g,
            "\t",
            [h for h in new_gates if h[-1] in g[0] and h[0][0][0] in ("x", "y")],
            "\t",
            [h for h in new_gates if h[-1] in g[0] and h[0][0][0] not in ("x", "y")]
        )

    swaps_flat = []
    for swap in swaps:
        for x in swap:
            swaps_flat.append(x)

    print(",".join(sorted(swaps_flat)))