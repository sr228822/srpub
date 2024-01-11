from collections import namedtuple

Rectangle = namedtuple("Rectangle", ["bottom", "top", "left", "right"])


def find_coverage(width, height, rectangles) -> float:
    # print(rectangles)
    for r in rectangles:
        print(r)

    verticals = set()
    horizontals = set()
    for r in rectangles:
        verticals.add(r.left)
        verticals.add(r.right)
        horizontals.add(r.top)
        horizontals.add(r.bottom)

    sorted_verticals = [0.0] + sorted(list(verticals)) + [width]
    sorted_horizontals = [0.0] + sorted(list(horizontals)) + [height]
    print(f"verticals: {sorted_verticals}")
    print(f"horizontals: {sorted_horizontals}")

    v_lookup = {v: i for i, v in enumerate(sorted_verticals)}
    h_lookup = {v: i for i, v in enumerate(sorted_horizontals)}
    print(f"v_lookup: {v_lookup}")
    print(f"h_lookup: {h_lookup}")

    grid = []
    for i in range(len(sorted_horizontals)):
        grid.append([0] * len(sorted_verticals))

    # grid = [[0]*len(v_lookup)]*len(h_lookup)

    def _print_grid():
        print("\n== grid ==")
        print(sorted_verticals)
        for ri, row in enumerate(grid):
            print(f"{sorted_horizontals[ri]} {row}")

    _print_grid()

    for r in rectangles:
        print(f"r:{r}")
        for vi in range(v_lookup[r.left], v_lookup[r.right]):
            for hi in range(h_lookup[r.bottom], h_lookup[r.top]):
                print(f"vi: {vi} hi: {hi}")
                grid[hi][vi] = 1
                print(grid)
    _print_grid()

    covered = 0.0
    for hi in range(len(sorted_horizontals)):
        for vi in range(len(sorted_verticals)):
            if grid[hi][vi]:
                print(
                    f"covered square hi: {hi} vi: {vi} {sorted_horizontals[hi+1]} {sorted_horizontals[hi]} {sorted_verticals[vi+1]} {sorted_verticals[vi]}"
                )
                covered += (sorted_horizontals[hi + 1] - sorted_horizontals[hi]) * (
                    sorted_verticals[vi + 1] - sorted_verticals[vi]
                )
    print(covered)
    return covered / (width * height)


width = 10.0
height = 5.0

rectangles = [
    # bottom, top, left, right
    Rectangle(0.2, 0.3, 0.4, 0.5),
    Rectangle(1.0, 3.0, 1.0, 3.0),
    Rectangle(1.0, 2.0, 1.0, 2.0),
    # Rectangle(2.0, 4.0, 1.0, 3.0),
    # Rectangle(1.0, 2.0, 1.0, 2.0),
]

print(find_coverage(width, height, rectangles))
