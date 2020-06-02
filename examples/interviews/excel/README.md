Excel / Google-Sheets
============

This question is designed to be fairly flexible and open-ended,
allowing different candidates to focus on different areas, and
adjusting to different levels (intern, new-grad, senior).

Part 2 and Part 3 are not interdependent.
Part 2 focuses on more complex datastructures and algorithms
where Part 3 focuses on web-service architecture/design.
A candidate could do either or both dependeing on their level,
skills, and interest.

## Part 1

Design a backend to support excel / google-sheets.

* Columns are lettered ("A", "B", "C", ...), Rows are numbered (1, 2, 3, ...)
* The backend can operate as a class, and does not need to load/save data to disk.
  New sheets can be initialized as empty
* The backend should support at least a `set` and `get` operation.  All data will
  be sent and strings and should be returned as strings.
* We do not need to support any style or formatting, just data operations.
* Formulas (any string starting with `=` sign, should be evaluated).  For simplicity
  we will only support addition in formulas.

Example Use:
```
>>> sheet = MySheet()

>>> sheet.set("A1", "hello")
>>> sheet.get("A1")
hello

>>> sheet.set("B2", "5")
>>> sheet.get("B2")
5

>>> sheet.set("A3", "=2+2")
>>> sheet.get("A3")
4
```

Resulting Sheet:
|   | A | B |
| - | - | - |
| 1 | hello |
| 2 |  | 5 |
| 3 | 4 | |

#### Common Questions:
You shouldn't necessary give this information up-front, but most candidates will end up asking
* <b>How many rows/columns should the sheet be?</b>  Infinite, or resizeable to arbitrary sizes.
  We should be able set cell `ZZZ99999` without it breaking.
* <b>Is the data sparse or dense?</b> Either
* <b>Can I use `eval` to calculate formulas?</b> Do you think that's wise?  What might be some risks of this?
* <b>What should a `get` on an empty cell return?</b>Null or empty-string
* <b>What should an invalid formulas do?</b>Throw an error/exception on set

#### Example Solution

See part1.py in this folder.

Some candiates will evaluate formulas on either the set or the get.
It doesn't really matter at this point, but will become important later.

#### Discussion
* The candidate should realize that a dict/hash-table is the best datastructure to use
  It's common to initially think of a array/list/2d-array since the sheet "looks"
  like a 2d-array, but once you realize that the data may be sparse, and that
  we want to support arbitrary sizes, the obvious memory-efficient O(1) solution
  is a dictionary.  If they choose any other datastructure, ask them about the
  memory-use or read/write access speed.
* For this part, they can get away without needing a `Cell` class
  by storing everything as a string.  Some un-typed languages (python)
  you can have a dict which stores arbitrary-mixed types, which is okay.
  There are many different solutions in different languages for storing
  different types of data which will become more relevant/necessary in later steps,
  but if they implement one here thats okay.

## Part 2
Extend your solution to support references to other cells in formulas.

Continuing our example from above...

```
>>> sheet.set("C3", "=B2+2")
>>> sheet.get("C3")
7
```

#### Part 2B
Some candidates will catch the extra implications that
* Cells with formulas referencing other cells should update if the cell they
  reference is updated
* Referenced cells might be formulas themselves, so its necessary to support
  recursive evaluation or solve this another way.

I do not usually point this out, I wait to see how they implement part 2 given
only the first example.  If they don't catch this on their own, then I will
give them the extra test-cases below.

```
>>> sheet.set("B2", "10")
>>> sheet.get("C3")
12

>>> sheet.set("B2", "=10+10")
>>> sheet.get("C3")
22
```

#### Example Solution

Two example solutions are provided:
* part2_lazy_recursive.py : A simpler but less efficient solution, which does
  redundant recursive calculation.
* part2_efficient.py : A complex but more efficient solution which builds a
  graph of cell dependencies, and only re-calculates where needed

#### Discussion
* Doing effient evaluation is tricky here, because you need to keep track of
  graph of relationships between cells, and only update cells when a cell they
  depend on gets updated.   The lazy solution is functionally correct, but
  would incur significant cost if there are larger graphs of cell dependencies.
* Lots of candidates get hung-up trying to create a Cell class, but then find
  that the cell class needs access to the overall data.  The efficient solution
  included gets around this by using a "dumb" cell class as a data-structure
  but keeping all calculation in the main methods

## Part 3 : Web-Service
Implement your solution as a web-service (like in Google-Sheets) that can support
multiple concurrent editors.

#### Example Solution
This part could go in many directions depending on the language or design decisions.
One example in python of a simple Flask service, with a multi-proces lock on set
is shown; but this example uses a global object for the sheet-data, so it would not
really work for multiple processes or multiple servers.

Candidates might also explore using a dummy DB, the structure of tables, and example
SQL operations.

See part3.py

#### Discussion
* Did they define a reasonable API
* Did they error check bad requests and return status codes?
  What about internal exceptions?
* How did they handle multiple-editors on a given cell?
* How was data stored?  If they used or described the use of a database, how was
  the data structured.  Was their choice of database reasonable?
* How would their solution scale?  How many QPS could it handle?  How many servers
  would we need?
* How would we monitor this service for corectnes? What metrics would we want?
  What alerts would we setup?
