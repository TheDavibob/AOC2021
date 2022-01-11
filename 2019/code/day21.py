import common
import intcode


class Ascii(intcode.Intcode):
    def run_on_ascii(self, ascii_command: str, print_output=True):
        for c in ascii_command:
            self.input_list.append(ord(c))

        if self.input_list[-1] != 10:
            self.input_list.append(10)

        self.step_all()

        if print_output:
            self.interpret_ascii(print_output=True)

    def interpret_ascii(self, print_output=True):
        output_string_as_list = []
        while self.output_list:
            c = self.output_list.pop(0)
            if c > 0x11000:
                output_string_as_list.append(str(c))
            else:
                output_string_as_list.append(chr(c))

        output_string = "".join(output_string_as_list)
        if print_output:
            print(output_string.replace('.', '_'))

        return output_string

    def reset(self):
        self.instruction_pointer = 0
        self.input_list = []
        self.output_list = []
        self.input_pointer = 0
        self.relative_base = 0

PART_1_STRING = """NOT A J
NOT B T
OR T J
NOT C T
OR T J
NOT D T
AND D J
WALK
"""

# The logic below:
# If A, E and I are free, walk
# If D and H are free, jump
# Unless A, B and C are all free too, in which case walk
# If A is gone, jump
PART_2_STRING = """OR D T
AND H T
OR E J
AND I J
AND A J
NOT J J
AND T J
NOT A T
OR T J
NOT T T
AND B T
AND C T
NOT T T
AND T J
RUN
"""


if __name__ == "__main__":
    code = common.import_file('../input/day21')
    s = Ascii(code, pause_on_no_inputs=True)
    s.run_on_ascii(PART_1_STRING)

    s = Ascii(code, pause_on_no_inputs=True)
    s.run_on_ascii(PART_2_STRING)
