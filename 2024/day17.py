class Computer:
    def __init__(self, register_A, register_B, register_C, instructions):
        self.A = register_A
        self.B = register_B
        self.C = register_C

        self.instructions = instructions
        self.instruction_pointer = 0

        self.return_values = []

    def step(self) -> bool:
        if self.instruction_pointer >= len(self.instructions):
            return True

        instruction = self.instructions[self.instruction_pointer]
        literal_operand = self.instructions[self.instruction_pointer + 1]
        combo_operand = self._look_up_combo_operand(literal_operand)

        self.instruction_pointer += 2

        if instruction == 0:
            # adv: Division
            numerator = self.A
            denominator = 1 << combo_operand
            self.A = numerator // denominator
        elif instruction == 1:
            # bxl: XOR
            self.B = self.B ^ literal_operand
        elif instruction == 2:
            # bst: mod
            self.B = combo_operand % 8
        elif instruction == 3:
            # jnz
            if self.A != 0:
                self.instruction_pointer = literal_operand
        elif instruction == 4:
            # bxc
            self.B = self.B ^ self.C
        elif instruction == 5:
            # out
            self.return_values.append(
                combo_operand % 8
            )
        elif instruction == 6:
            numerator = self.A
            denominator = 1 << combo_operand
            self.B = numerator // denominator
        elif instruction == 7:
            numerator = self.A
            denominator = 1 << combo_operand
            self.C = numerator // denominator
        else:
            raise ValueError(f"Instruction {instruction} not understood")

        return False

    def _look_up_combo_operand(self, operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C
        elif operand == 7:
            raise ValueError("Operand should not be 7")
        else:
            raise ValueError("Operand not between 0 and 8")

    def single_cycle(self, start_A):
        self.A = start_A
        self.B = 0
        self.C = 0
        self.instruction_pointer = 0
        self.return_values = []

        self.step()
        is_finished = False
        while self.instruction_pointer > 0:
            is_finished = self.step()
            if is_finished:
                break

        return is_finished, self.return_values[0], self.A


def tabulate_return_values(comp, start, end):
    finished = []
    return_val = []
    rem_A = []
    for i in range(start, end):
        d, v, a = comp.single_cycle(i)
        finished.append(d)
        return_val.append(v)
        rem_A.append(a)
    return finished, return_val, rem_A


def ramp_up(comp, target_sequence):
    current_number = 0
    A_sequentially = []
    attempts_at = []

    i = 0
    while i < len(target_sequence):
        target_value = target_sequence[-(i+1)]

        finished, values, rem_A = tabulate_return_values(
            comp,
            current_number * (1<<3) + 0,
            current_number * (1<<3) + 8,
        )

        options = [i for i, v in enumerate(values) if v == target_value]
        print(i, len(options))
        if i in [6]:
            # Hack because I couldn't be bothered to do this manually
            best = options[1]
        else:
            best = options[0]

        A_sequentially.append(best)
        current_number = current_number * (1<<3) + best

        i += 1

    return current_number


if __name__ == "__main__":
    with open("input/day17") as file:
        text = file.read()

    registers, program = text.split("\n\n")
    abc = []
    for line in registers.split("\n"):
        abc.append(int(line.split(": ")[-1]))

    instructions = [int(x) for x in program.split(": ")[-1].split(",")]
    comp = Computer(*abc, instructions)

    is_finished = False
    while not is_finished:
        is_finished = comp.step()

    print("Part 1:", ",".join(str(x) for x in comp.return_values))

    # What does the program do?
    # 2,4,1,1,7,5,4,0,0,3,1,6,5,5,3,0
    # 2,4: B = A % 8
    # 1,1: B = B ^ 1
    # 7,5: C = A // 2**B
    # 4,0: B = B ^ C
    # 0,3: A = A // 8
    # 1,6: B = B ^ 6
    # 5,5: out: B
    # 3,0: Start again unless A 0
    # So:
    # B and C are always reset each loop, so can sort of do this loop by loop:
    # Also: A is getting rapidly smaller: aside from the fiddly 7,5 we just need each three bits in turn
    finished, values, rem_A = tabulate_return_values(comp, 0, 8)

    # This tells us the first three bits are 7
    best_A = ramp_up(comp, instructions)