"""
This solution is more complicated, but efficient
because it will not re-do computation on get calls
"""


class Cell:
    def __init__(self):
        self.raw = None
        self.value = None

        # A map containing the addrs of all cells
        # referencing this one
        self.dependents = {}

    def set(self, raw):
        self.raw = raw
        self.is_form = is_formula(raw)

    def value(self):
        return self.val or 0


def is_formula(v):
    return v.strip().startswith("=")


def is_number(v):
    try:
        int(v)
        return True
    except:
        return False


class MySheet:
    def __init__(self):
        self.data = {}

    def _eval_formula(self, addr, v):
        r = v.strip().lstrip("=")
        terms = [x.strip() for x in r.split("+")]
        s = 0
        for x in terms:
            if is_number(x):
                s += int(x)
            else:
                # if its not a number, it must be a cell-addr
                other = self.data.get(x, None)
                # if referenced cell doesnt exit, create it
                if not other:
                    other = Cell()
                    self.data[x] = other
                # Put this cell as a dependent of the other
                if other:
                    s += other.value or 0
                    other.dependents[addr] = True

        return s

    def _update(self, addr, value=None, loop_orig=None):
        if not loop_orig:
            # this is the first update, mark ourself as the start of the loop
            loop_orig = addr
        else:
            if addr == loop_orig:
                raise Exception("Cycle Error")

        # get existing cell, or create one
        c = self.data.get(addr, Cell())
        if value:
            c.raw = value

        # set value from the raw
        if is_number(c.raw):
            c.value = int(c.raw)
        elif is_formula(c.raw):
            c.value = self._eval_formula(addr, c.raw)
        else:
            c.value = str(c.raw)

        # update dependents
        for dep in c.dependents.keys():
            self._update(dep, loop_orig=loop_orig)

        self.data[addr] = c

    def set(self, addr, value):
        # get existing cell, or create one
        self._update(addr, value=value)

    def get(self, addr):
        c = self.data.get(addr, None)
        return c.value if c else ""


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

print("\nhard mode, refernces to not-yet-existent cells")
sheet.set("F4", "=F5+2")
print("F4 should be 2:", sheet.get("F4"))
sheet.set("F5", "3")
print("F4 should be 5:", sheet.get("F4"))

print("\nhard mode, unusual spacing, high addresses")
sheet.set("ZZZZDF22222", "3")
sheet.set("ZZZZB12312", " =        ZZZZDF22222  +    2")
print("ZZZZB12312 should be 5:", sheet.get("ZZZZB12312"))

print("\nhard mode, branching, merging, double references")
sheet.set("K1", "2")
sheet.set("K2", "=K1+K1+2")
sheet.set("K3", "=K1+2")
sheet.set("K4", "=K2+K3+K1")
print("K4 should be 12:", sheet.get("K4"))
sheet.set("K1", "1")
print("K4 should be 8:", sheet.get("K4"))

print("\nhard mode, cycle detection")
sheet.set("Q1", "=Q2+2")
sheet.set("Q2", "=Q3+2")
did_error = False
try:
    sheet.set("Q3", "=Q1+2")
except Exception as e:
    did_error = True
    print(f"Did correctly error: {e}")
if not did_error:
    print("Should have errored for cycle, but did not")
