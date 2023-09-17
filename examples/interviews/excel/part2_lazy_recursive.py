"""
This solution is simple, but in-efficient because it
re-does compuation on every get-call, and because
it re-does formula evluation of common dependencies.

However this laziness lets it easily solve the 2b issues
"""
import re


def is_formula(v):
    return type(v) == str and v.strip().startswith("=")


class MySheet:
    def __init__(self):
        self.data = {}

    def _as_number(self, thing):
        """Try an interpret thing as a number"""
        if thing.isnumeric():
            return int(thing)

        # if its not a number, it must be a cell-addr
        assert re.match("^[A-Z]+\d+$", thing)

        return int(self.get(thing, default=0))

    def _eval_formula(self, v):
        terms = v.split("+")
        as_ints = [self._as_number(x.strip()) for x in terms]
        return sum(as_ints)

    def set(self, addr, value):
        self.data[addr] = str(value)

    def get(self, addr, default=""):
        val = self.data.get(addr, default)
        if is_formula(val):
            return self._eval_formula(val.strip()[1:])
        return val


sheet = MySheet()

sheet.set("A1", "hello")
print("A1 should be hello:", sheet.get("A1"))

sheet.set("B2", "5")
print("B2 should be 5:", sheet.get("B2"))

sheet.set("A3", "=2+2")
print("A3 should be 4", sheet.get("A3"))

sheet.set("C3", "=B2+2")
print("C3 should be 7:", sheet.get("C3"))

sheet.set("B2", "=10")
print("C3 should be 12", sheet.get("C3"))

sheet.set("B2", "=10+10")
print("C3 should be 22:", sheet.get("C3"))

# some edge-cases around formulas
sheet.set("D1", " = 5 + C3 + EZ88")
print("D1 should be 27", sheet.get("D1"))
