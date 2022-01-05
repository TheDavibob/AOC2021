import common


def add_snailfish(list1, list2):
    added = [list1, list2]
    return added


def explode(snailfish):
    left = tuple()
    to_add = None
    for i, a in enumerate(snailfish):
        if isinstance(a, int):
            left = (i,)
            if to_add is not None:
                snailfish[i] += to_add
                return True
            continue
        for j, b in enumerate(a):
            if isinstance(b, int):
                left = (i, j)
                if to_add is not None:
                    snailfish[i][j] += to_add
                    return True
                continue
            for k, c in enumerate(b):
                if isinstance(c, int):
                    left = (i, j, k)
                    if to_add is not None:
                        snailfish[i][j][k] += to_add
                        return True
                    continue
                for l, d in enumerate(c):
                    if isinstance(d, int):
                        left = (i, j, k, l)
                        if to_add is not None:
                            snailfish[i][j][k][l] += to_add
                            return True
                        continue

                    if to_add is None:
                        if left:
                            if len(left) == 1:
                                snailfish[left[0]] += d[0]
                            elif len(left) == 2:
                                snailfish[left[0]][left[1]] += d[0]
                            elif len(left) == 3:
                                snailfish[left[0]][left[1]][left[2]] += d[0]
                            elif len(left) == 4:
                                snailfish[left[0]][left[1]][left[2]][left[3]] += d[0]

                        to_add = d[1]
                        c[l] = 0
                        continue

                    if to_add is not None:
                        for m, e in enumerate(d):
                            if isinstance(e, int):
                                snailfish[i][j][k][l][m] += to_add
                                return True

    if to_add is not None:
        return True
    else:
        return False


def split_line(line):
    for i, a in enumerate(line):
        if isinstance(a, int):
            if a >= 10:
                line[i] = [a//2, a-a//2]
                return True
        else:
            success = split_line(a)
            if success:
                return True

    return False


def add_snailfish_list(snailfish_list):
    list_so_far = eval(snailfish_list[0])
    for l in snailfish_list[1:]:
        new_list = eval(l)
        list_so_far = add_snailfish(list_so_far, new_list)
        processing = True
        while processing:
            processing = explode(list_so_far)
            if not processing:
                processing = split_line(list_so_far)

    return list_so_far


def magnitude(thing):
    if isinstance(thing, int):
        return thing
    else:
        return 3*magnitude(thing[0]) + 2 * magnitude(thing[1])


def main(input):
    snailfish_list = [l for l in input.split('\n') if l != ""]
    part_1 =  magnitude(add_snailfish_list(snailfish_list))
    part_2 = pairwise_addition(snailfish_list)
    return part_1, part_2


def pairwise_addition(snailfish_list):
    max_mag = 0
    max_list = (None, None)
    for i, l1 in enumerate(snailfish_list):
        for j, l2 in enumerate(snailfish_list):
            if i == j:
                continue
            mag = magnitude(add_snailfish_list([l1, l2]))
            if mag > max_mag:
                max_mag = mag
                max_list = (l1, l2)

    return max_mag, max_list



if __name__ == "__main__":
    input = common.import_file('input/day18_input')
    part_1, part_2 = main(input)
    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2[0]}")