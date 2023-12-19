# Copyright (C) Cambridge Consultants Ltd 2023
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import itertools
from functools import cache

import common
import numpy as np
from tqdm import tqdm


def parse_input(text):
    return text.split(",")


def get_hash(char_string):
    current_value = 0
    for char in char_string:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256

    return current_value


def part_one(strings):
    total = 0
    for string in strings:
        total += get_hash(string)
    return total


def part_two(strings):
    boxes = [[] for _ in range(256)]
    for string in strings:
        if "=" in string:
            operation = "="
        elif "-" in string:
            operation = "-"
        else:
            raise ValueError("No operation?")

        label, focal_length = string.split(operation)
        if focal_length:
            focal_length = int(focal_length)
        box = get_hash(label)

        try:
            label_idx = [labs for (labs, focs) in boxes[box]].index(label)
            if operation == "-":
                boxes[box].pop(label_idx)
            elif operation == "=":
                boxes[box][label_idx] = (label, focal_length)
        except ValueError:
            if operation == "=":
                boxes[box].append((label, focal_length))

    focusing_power = 0
    for i_box, box in enumerate(boxes):
        box_value = i_box + 1
        for i_lens, (lens, focal_length) in enumerate(box):
            slot_value = i_lens + 1
            focusing_power += slot_value * box_value * focal_length

    return focusing_power


if __name__ == "__main__":
    text = common.import_file("input/day15")
    demo_text = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

    assert get_hash("HASH") == 52

    assert part_one(parse_input(demo_text)) == 1320

    common.part(1, part_one(parse_input(text)))

    assert part_two(parse_input(demo_text)) == 145

    common.part(2, part_two(parse_input(text)))