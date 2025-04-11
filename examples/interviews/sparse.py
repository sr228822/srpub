from pprint import pformat

debug = False


def dprint(txt):
    if debug:
        print(txt)


def snake_traverse(triplets: list[tuple], rows: int, cols: int):
    # Lets put tripplets into a dict for quick lookup
    triplet_lookup = {}
    for triplet in triplets:
        triplet_lookup[(triplet[0], triplet[1])] = triplet[2]
    dprint(pformat(triplet_lookup))

    res = []
    # first row move right
    forward = True
    for row in range(rows):
        for col in range(cols):
            # when moving backwords revser the cols order
            col = col if forward else cols - col - 1
            index = (row, col)
            dprint(f"traversing {index}")
            val = triplet_lookup.get(index, 0)
            res.append(val)
        forward = not forward
    return res


# 1 0 2 0
# 0 3 0 0
# 4 0 0 5
# 0 0 6 0

triplets = [(0, 0, 1), (0, 2, 2), (1, 1, 3), (2, 0, 4), (2, 3, 5), (3, 2, 6)]
result = snake_traverse(triplets, 4, 4)
print(result)
expected = [1, 0, 2, 0, 0, 0, 3, 0, 4, 0, 0, 5, 0, 6, 0, 0]
assert result == expected, result

# The snake pattern traversal would visit positions in this order:
# Row 0: (0,0) → (0,1) → (0,2) → (0,3)  [Right]
# Row 1: (1,3) → (1,2) → (1,1) → (1,0)  [Left]
# Row 2: (2,0) → (2,1) → (2,2) → (2,3)  [Right]
# Row 3: (3,3) → (3,2) → (3,1) → (3,0)  [Left]


triplets = []
result = snake_traverse(triplets, 3, 3)
print(result)
expected = [0, 0, 0, 0, 0, 0, 0, 0, 0]
print(expected)
assert result == expected, result


result = snake_traverse([], 0, 0)
assert result == []
