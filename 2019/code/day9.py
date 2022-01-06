import intcode
import common

text = common.import_file("../input/day9")
print(intcode.run_intcode(text, [1])[1][0])
print(intcode.run_intcode(text, [2])[1])