class Intcode:
    def __init__(self, intcode):
        if isinstance(intcode, str):
            self.code = [int(s) for s in intcode.split(',')]
        else:
            self.code = intcode
        self.instruction_pointer = 0

    def step(self):
        opcode = self.code[self.instruction_pointer]
        if opcode not in [1, 2, 99]:
            raise ValueError(f"Unexpected opcode: {opcode}")

        pointer_1 = self.code[self.instruction_pointer + 1]
        pointer_2 = self.code[self.instruction_pointer + 2]
        pointer_3 = self.code[self.instruction_pointer + 3]

        n_parameters = 0
        if opcode == 1:
            n_parameters = 3
            self.code[pointer_3] = self.code[pointer_1] + self.code[pointer_2]
        elif opcode == 2:
            n_parameters = 3
            self.code[pointer_3] = self.code[pointer_1] * self.code[pointer_2]
        elif opcode == 99:
            n_parameters = 0
            return True

        self.instruction_pointer += n_parameters + 1

        return False

    def step_all(self):
        finished = False
        while not finished:
            finished = self.step()


def test_day_2():
    test_input = "1,9,10,3,2,3,11,0,99,30,40,50"
    s = Intcode(test_input)
    s.step_all()
    expected = """3500,9,10,70,
2,3,11,0,
99,
30,40,50"""
    expected = expected.replace("\n", "")
    assert s.code == [int(s) for s in expected.split(',')]