
def step(numbers_dict):
    new_dict = {}
    for key, value in numbers_dict.items():
        if key == 0:
            new_keys = [1]
        elif len(str(key)) % 2 == 0:
            as_str = str(key)
            new_keys = [int(as_str[:len(as_str) // 2]), int(as_str[len(as_str) // 2:])]
        else:
            new_keys = [key * 2024]

        for new_key in new_keys:
            if new_key in new_dict:
                new_dict[new_key] += value
            else:
                new_dict[new_key] = value

    return new_dict


if __name__ == "__main__":
    with open("input/day11") as file:
        text = file.read()

    # text = "125 17"

    initial_list = [int(x) for x in text.split(" ")]
    as_dict = {x: 1 for x in initial_list}
    for _ in range(25):
        as_dict = step(as_dict)
    print(f"Part 1: {sum(as_dict.values())}")

    for _ in range(50):
        as_dict = step(as_dict)
    print(f"Part 2: {sum(as_dict.values())}")
