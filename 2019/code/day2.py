import common
import intcode

text = common.import_file("../input/day2")
text = text.replace('\n', '')

code = [int(s) for s in text.split(',')]

code[1] = 12
code[2] = 2

s = intcode.Intcode(code)
s.step_all()
print(f"Part 1: {s.code[0]}")

for noun in range(100):
    for verb in range(100):
        code = [int(s) for s in text.split(',')]
        code[1] = noun
        code[2] = verb

        s = intcode.Intcode(code)
        s.step_all()
        if s.code[0] == 19690720:
            print(f"Part 2: {100*noun + verb}")
            break
