#!/usr/bin/python

class Cell:
    def __init__(self, val):
        self.raw = val

    def __str__(self):
        if not self.raw:
            return ""
        return str(self.raw)


class Sheet:
    def __init__(self):
        self.cells = {}

    def set(self, cell, val):
        self.cells[cell] = Cell(val)

    def read(self, cell):
        c = self.cells.get(cell, Cell(None))
        return str(c)



s = Sheet()

s.set("A2", "5")
print "A2", s.read("A2")

s.set("A3", "hello")
print "A3", s.read("A3")

print "B5", s.read("B5")
