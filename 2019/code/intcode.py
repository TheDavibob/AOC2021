class Intcode:
    def __init__(self, intcode, input_list=None, pause_on_no_inputs=False):
        if isinstance(intcode, str):
            self.code = [int(s) for s in intcode.split(',')]
        else:
            self.code = intcode
        self.instruction_pointer = 0

        if input_list is None:
            self.input_list = []
        else:
            self.input_list = input_list
        self.input_pointer = 0

        self.pause = pause_on_no_inputs

        self.output_list = []

    def step(self):
        opcode_and_parameter_code = self.code[self.instruction_pointer]
        opcode = opcode_and_parameter_code % 100
        parameter_code = opcode_and_parameter_code // 100
        if opcode not in [1, 2, 3, 4, 5, 6, 7, 8, 99]:
            raise ValueError(f"Unexpected opcode: {opcode}")

        n_parameters = 0
        increment = True
        if opcode == 1:
            n_parameters = 3
            parameters = self.get_parameters(n_parameters, parameter_code, write=True)
            self.code[parameters[-1]] = parameters[0] + parameters[1]
        elif opcode == 2:
            n_parameters = 3
            parameters = self.get_parameters(n_parameters, parameter_code, write=True)
            self.code[parameters[-1]] = parameters[0] * parameters[1]
        elif opcode == 3:
            n_parameters = 1
            parameters = self.get_parameters(n_parameters, parameter_code, write=True)
            if self.input_pointer == len(self.input_list):
                if self.pause:
                    return 2
                else:
                    new_input = int(input("Enter a value"))
            else:
                new_input = self.input_list[self.input_pointer]
                self.input_pointer += 1

            self.code[parameters[-1]] = new_input
        elif opcode == 4:
            n_parameters = 1
            parameters = self.get_parameters(n_parameters, parameter_code, write=False)
            self.output_list.append(parameters[0])
        elif opcode == 5:
            n_parameters = 2
            parameters = self.get_parameters(n_parameters, parameter_code, write=False)
            if parameters[0] != 0:
                self.instruction_pointer = parameters[1]
                increment = False
        elif opcode == 6:
            n_parameters = 2
            parameters = self.get_parameters(n_parameters, parameter_code, write=False)
            if parameters[0] == 0:
                self.instruction_pointer = parameters[1]
                increment = False
        elif opcode == 7:
            n_parameters = 3
            parameters = self.get_parameters(n_parameters, parameter_code, write=True)
            self.code[parameters[-1]] = int(parameters[0] < parameters[1])
        elif opcode == 8:
            n_parameters = 3
            parameters = self.get_parameters(n_parameters, parameter_code, write=True)
            self.code[parameters[-1]] = int(parameters[0] == parameters[1])
        elif opcode == 99:
            n_parameters = 0
            return 1

        if increment:
            self.instruction_pointer += n_parameters + 1

        return 0

    def get_parameters(self, n_parameters, parameter_code, write=True):
        parameter_code = str(parameter_code).rjust(n_parameters, '0')[::-1]
        parameters = []
        for i, code in enumerate(parameter_code):
            if write and (i == n_parameters - 1):
                # Return the write pointer, rather than the value stored there
                parameters.append(self.code[self.instruction_pointer + i + 1])
            elif int(code) == 0:
                parameters.append(self.code[self.code[self.instruction_pointer + i + 1]])
            elif int(code) == 1:
                parameters.append(self.code[self.instruction_pointer + i + 1])
            else:
                ValueError("Code not understood")

        return parameters

    def step_all(self):
        status = 0
        while status == 0:
            status = self.step()

        if status == 1:
            # Finished
            return 0
        else:
            # Merely pausing
            return 1


def run_intcode(intcode, input_list=None):
    s = Intcode(intcode, input_list)
    s.step_all()
    return s.code, s.output_list


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


def test_day_5():
    input = "3,0,4,0,99"
    s = run_intcode(input)
