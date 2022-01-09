import common


def deal(current_position, pack_length):
    return -(current_position+1) % pack_length


def cut(n, current_position, pack_length):
    return (current_position - n) % pack_length


def increment(n, current_position, pack_length):
    return current_position * n % pack_length


def iterate_through_instructions(instructions, pack_length, card_to_track):
    current_position = card_to_track
    for instruction in instructions.split('\n'):
        if instruction == "":
            continue

        if instruction == "deal into new stack":
            current_position = deal(current_position, pack_length)
        elif ' '.join(instruction.split(' ')[:-1]) == "deal with increment":
            n = int(instruction.split(' ')[-1])
            current_position = increment(n, current_position, pack_length)
        elif instruction.split(' ')[0] == "cut":
            n = int(instruction.split(' ')[-1])
            current_position = cut(n, current_position, pack_length)
        else:
            ValueError(f"Instruction {instruction} not understood")

    return current_position


def clever_cut(n, constant, multiple):
    constant -= n
    return constant, multiple


def clever_increment(n, constant, multiple):
    constant *= n
    multiple *= n
    return constant, multiple


def clever_deal(constant, multiple):
    constant, multiple = clever_cut(-1, constant, multiple)
    constant, multiple = clever_increment(-1, constant, multiple)
    return constant, multiple


def clever_instruction(instructions):
    constant = 0
    multiple = 1
    for instruction in instructions.split('\n'):
        if instruction == "":
            continue

        if instruction == "deal into new stack":
            constant, multiple = clever_deal(constant, multiple)
        elif ' '.join(instruction.split(' ')[:-1]) == "deal with increment":
            n = int(instruction.split(' ')[-1])
            constant, multiple = clever_increment(n, constant, multiple)
        elif instruction.split(' ')[0] == "cut":
            n = int(instruction.split(' ')[-1])
            constant, multiple = clever_cut(n, constant, multiple)
        else:
            ValueError(f"Instruction {instruction} not understood")

    return constant, multiple


def mod_exp(a, b, base):
    # computes a**b mod base
    bin_b = bin(b)
    power_so_far = a
    cumulant = 1
    i = 0
    for i in range(len(bin_b) - 1):
        if bin_b[-(i+1)] == "1":
            cumulant *= power_so_far
            cumulant %= base

        power_so_far *= power_so_far
        power_so_far %= base

    return cumulant


def mod_geometric(a, b, base):
    if b == 1:
        return 1
    elif b == 2:
        return (1 + a) % base
    else:
        if b % 2 == 0:
            output = ((1 + a) * mod_geometric(a**2 % base, b // 2, base)) % base
        else:
            output = ((1 + a) * mod_geometric(a**2 % base, (b - 1) // 2, base)) % base + mod_exp(a, (b-1), base)

        return output


if __name__ == "__main__":
    instructions = common.import_file('../input/day22')
    common.part(1, iterate_through_instructions(instructions, 10007, 2019))

    current_position = 2020
    # for i in range(101741582076661):
    #     current_position = iterate_through_instructions(instructions, 119315717514047, current_position)
    #     if current_position == 2020:
    #         loop_time = i
    #         break

    # deal == : cut by -1, increment by -1
    # cut subtracts, increment multiplies
    # so keep track of subtraction amount, and multiple (noting that multiple multplies increment too)

    constant, multiple = clever_instruction(instructions)
    # New position is multiple*old_position + constant
    common.part(1, (2019*(multiple % 10007) + (constant % 10007)) % 10007)

    n_cards = 119315717514047
    n_reps = 101741582076661

    constant = constant % n_cards
    multiple = multiple % n_cards

    super_multiple = mod_exp(multiple, n_reps, n_cards)
    super_constant = (constant * mod_geometric(multiple, n_reps, n_cards)) % n_cards

    # Oops, python can already do the pow bit
    inverse_thing = pow(super_multiple, -1, mod=n_cards)

    # We need the ax + b = 2020, which is done via the below
    common.part(2, (inverse_thing * (2020 - super_constant)) % n_cards)