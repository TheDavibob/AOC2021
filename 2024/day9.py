import numpy as np

with open("input/day9") as file:
    text = file.read()

total = sum(int(x) for x in text)
print(total)

as_array = np.zeros(total-1, dtype=int)
n_slots = len(text) // 2
current_position = 0
for i in range(n_slots):
    next_slot = int(text[2*i])
    as_array[current_position:current_position+next_slot] = i
    current_position = current_position + next_slot

    next_gap = int(text[2*i+1])
    as_array[current_position:current_position+next_gap] = -1
    current_position = current_position + next_gap

assert(current_position == total-1)