"""
This solution is more complicated, but efficient
because it will not re-do computation on get calls
"""


from dataclasses import dataclass, field


@dataclass
class Cell:
    raw: str = None
    value: str = None
    dependents: dict[str, str] = field(default_factory=dict)


class MySheet:
    def __init__(self):
        self.data: [str, Cell] = {}

    def _eval_formula(self, addr, v) -> int:
        terms = v.lstrip("=").split("+")
        s = 0
        for x in terms:
            if x.isnumeric():
                s += int(x)
            else:
                # if its not a number, it must be a cell-addr
                other = self.data.get(x, None)

                # Put this cell as a dependent of the other
                if other:
                    s += int(other.value)
                    other.dependents[addr] = True

        return s

    def _update(self, addr, value=None):
        # get existing cell, or create one
        c = self.data.get(addr, Cell())
        if value:
            c.raw = value

        # put value from the raw
        if c.raw.startswith("="):
            c.value = str(self._eval_formula(addr, c.raw))
        else:
            c.value = c.raw

        # update dependents
        for dep in c.dependents.keys():
            self._update(dep)

        self.data[addr] = c

    def put(self, addr, value):
        # get existing cell, or create one
        self._update(addr, value=value)

    def get(self, addr):
        c = self.data.get(addr, None)
        return c.value if c else ""


def _test(sheet, addr, expected, annotation=""):
    val = sheet.get(addr)
    msg = f"{addr} should be {expected} ({type(expected)}) is {val} ({type(expected)}) : ({annotation})"
    if val != expected:
        assert val == expected, msg
    else:
        print(f"[PASS] {msg}")


def test_part2():
    sheet = MySheet()

    sheet.put("A1", "hello")
    _test(sheet, "A1", "hello")

    sheet.put("B2", "5")
    _test(sheet, "B2", "5")

    sheet.put("A3", "=2+2")
    _test(sheet, "A3", "4")

    sheet.put("C3", "=B2+2")
    _test(sheet, "C3", "7")

    sheet.put("B2", "=10")
    _test(sheet, "C3", "12", "updated formula reference")

    sheet.put("B2", "=10+10")
    _test(sheet, "C3", "22", "nested formulas")


if __name__ == "__main__":
    test_part2()
