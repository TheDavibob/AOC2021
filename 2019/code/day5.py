import common
from intcode import run_intcode

text = common.import_file("../input/day5")
output_list = run_intcode(text, [1])[1]
print(f"Part 1: {output_list}")

output_list = run_intcode(text, [5])[1]
print(f"Part 2: {output_list}")