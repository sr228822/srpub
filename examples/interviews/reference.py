# Basic reminders
1. TALK
2. Ask clarifying question / requirements
3. discuss multiple solutions / tradeoffs
4. if stuck finding best, write something
5. comments, docstrings
6. writes tests

################################
#  Dataclass

Common strategies:
  - iterate in reverse
  - iterate on the alternate variable
  - use a dictionary vs an array
  - hash strings for comparison, faster, less mem

################################
#  Dataclass
from dataclasses import dataclass

@dataclass
class Point:
    """Class for keeping track of an item in inventory."""
    name: str
    lat: float
    lng: float

p = Point("test", 4.4, 5.5)

################################
# Named Tuples
from collections import namedtuple
Point = namedtuple('Point', 'x y')
p = Point(1.0, 5.0)
print(p.x)


################################
# Default Dict
from collections import defaultdict
data = defaultdict(list)
data['fruits'].append('apple')

# Hash string to shard-int
hash(txt) % 10


################################
# Custom field sort

mylist.sort(key=lambda x: x.foo)

# Regexes
txt = "The rain in Spain"

x = re.search("^The(.*)Spain$", txt)
    'rain in'

x = re.findall("ai", "The rain in Spain")
    ['ai', 'ai']


################################
# Timestamps

from datetime import datetime
now = datetime.now()

dt = datetime.fromisoformat("2024-11-01T09:00:00")

print(now.strftime("%Y-%m-%d %H:%M:%S"))
    '2021-03-07 23:16:41'

dt = datetime.strptime("09/23/2030 8:28","%m/%d/%Y %H:%M")

################################
# Threading lock

lock = threading.Lock()
lock.acquire()
count += 1
lock.release()

# or
with lock:
    count += 1

################################
# Test case loop

from collections import namedtuple
Testcase = namedtuple("Testcase", ['input', 'expected'])

tests = [
    Testcase("apple", "pp"),
    Testcase("bannanna", "nnnn"),
]

for testcase in tests:
    output = my_funtion(testcase.input)
    res = "FAIL" if output != testcase.expected else "SUCCESS"
    print(f"[{res}] test={testcase} output={output}")


################################
# Argparse
parser = argparse.ArgumentParser(description='My program')
parser.add_argument("positional", help="A positional arg")
parser.add_argument('-f','--flag', help='Description flag', required=True)
parser.add_argument("--verbose", action="store_true", help="Verbose debug logs")
args = parser.parse_args()
print(args.verbose)


################################
# Multi-threading / Multi-processing
CPU Bound => Multi Processing
I/O Bound, Fast I/O, Limited Number of Connections => Multi Threading
I/O Bound, Slow I/O, Many connections => Asyncio
