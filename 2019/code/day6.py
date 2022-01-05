import common


def parse_input(text):
    orbit_dict = {}
    for line in text.split('\n'):
        if line == "":
            continue
        inner, outer = line.split(')')
        orbit_dict[outer] = inner

    return orbit_dict


def count_upwards(key, orbit_dict):
    count = 1
    father_object = orbit_dict[key]
    while father_object != "COM":
        father_object = orbit_dict[father_object]
        count += 1

    return count


def count_all_upwards(orbit_dict):
    count = 0
    for v in orbit_dict.keys():
        count += count_upwards(v, orbit_dict)

    return count


def get_chain(target, orbit_dict):
    chain = [target]
    father_object = orbit_dict[target]
    chain.append(father_object)
    while father_object != "COM":
        father_object = orbit_dict[father_object]
        chain.append(father_object)

    return chain

def get_santa_you_dist(orbit_dict):
    santa_chain = get_chain("SAN", orbit_dict)
    you_chain = get_chain("YOU", orbit_dict)

    for i, el in enumerate(santa_chain):
        if el in you_chain:
            first_common_element = el
            santa_to_common = i
            break

    for i, el in enumerate(you_chain):
        if el == first_common_element:
            you_to_common = i

    return santa_to_common + you_to_common - 2

if __name__ == "__main__":
    text = common.import_file("../input/day6")
    orbit_dict = parse_input(text)
    print(count_all_upwards(orbit_dict))

    print(get_santa_you_dist(orbit_dict))