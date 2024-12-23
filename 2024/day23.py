from tqdm import tqdm


def parse_input(text):
    connections_dict = {}
    for line in text.split("\n"):
        if line == "":
            continue

        left, right = line.split("-")
        if left in connections_dict:
            connections_dict[left].append(right)
        else:
            connections_dict[left] = [right]

        if right in connections_dict:
            connections_dict[right].append(left)
        else:
            connections_dict[right] = [left]

    return connections_dict


def find_triples(connections):
    triples = []
    for left, rights in connections.items():
        for right in rights:
            for other in connections[right]:
                if other in rights:
                    triple = tuple(sorted((left, right, other)))
                    triples.append(triple)

    return list(set(triples))


def reduce_to_containing_t(triples):
    with_t = []
    for triple in triples:
        for x in triple:
            if x[0] == "t":
                with_t.append(triple)
                break

    return with_t


def find_next_size_up(connections, tuples):
    super_tuples = []
    for t in tqdm(tuples):
        shared = None
        for x in t:
            if shared is None:
                shared = set(connections[x])
            else:
                shared = shared.intersection(connections[x])

        if len(shared) > 0:
            for s in shared:
                super_tuple = tuple(sorted(t + (s,)))
                super_tuples.append(super_tuple)
    return list(set(super_tuples))



if __name__ == "__main__":
    with open("input/day23") as file:
        text = file.read()

    connections = parse_input(text)
    triples = find_triples(connections)
    with_t = reduce_to_containing_t(triples)
    print(f"Part 1: {len(with_t)}")

    quads = find_next_size_up(connections, triples)
    super_tuples = quads
    while len(super_tuples) > 1:
        super_tuples = find_next_size_up(connections, super_tuples)
        print(len(super_tuples[0]), len(super_tuples))
    print(f"part 2: {','.join(super_tuples[0])}")