import json

import numpy as np
import common


def build_up_directory(text):
    dir_list = {r"/": {}}
    ls_mode = False
    current_dir = [r"/"]

    for line in text.split("\n"):
        if line == "":
            continue

        elif line == r"$ cd /":
            ls_mode = False
            continue

        elif line == r"$ ls":
            ls_mode = True
            continue

        elif line.split(" ")[0] != "$":
            if not ls_mode:
                print("Expected ls_mode")

            loc = dir_list[current_dir[0]]
            for dir in current_dir[1:]:
                loc = loc[dir]

            num, fname = line.split(" ")

            try:
                num = int(num)
                loc[fname] = int(num)
            except ValueError:
                loc[fname] = {}

            continue

        elif line == "$ cd ..":
            ls_mode = False
            current_dir.pop()

        elif line.split(" ")[1] == "cd":
            ls_mode = False
            loc = dir_list[current_dir[0]]
            for dir in current_dir[1:]:
                loc = loc[dir]

            new_dir = line.split(" ")[2]
            loc[new_dir] = {}
            current_dir.append(new_dir)

    return dir_list


def size_folder(dir_structure):
    total = 0
    for k, v in dir_structure.items():
        if isinstance(v, int):
            total += v
        else:
            total += size_folder(v)

    return total


def get_all_dir_sizes(dir_structure):
    dir_sizes = [size_folder(dir_structure)]
    for k, v in dir_structure.items():
        if not isinstance(v, int):
            dir_sizes = dir_sizes + get_all_dir_sizes(v)

    return dir_sizes


if __name__ == "__main__":
    text = common.load_todays_input(__file__)
    dir_list = build_up_directory(text)

    all_sizes = get_all_dir_sizes(dir_list)
    small = sum(size for size in all_sizes if size <= 100000)

    common.part(1, small)

    total_size = size_folder(dir_list)
    total_space = 70000000
    required_space = 30000000

    to_remove = min(size for size in all_sizes if (total_size - size + required_space) <= total_space)

    common.part(2, to_remove)
