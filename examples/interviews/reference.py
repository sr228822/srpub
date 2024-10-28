# Dataclass
from dataclasses import dataclass

@dataclass
class Point:
    """Class for keeping track of an item in inventory."""
    name: str
    lat: float
    lng: float

p = Point("test", 4.4, 5.5)

# Named Tuples
from collections import namedtuple
Point = namedtuple('Point', 'x y')
p = Point(1.0, 5.0)
print(p.x)


# Default Dict
from collections import defaultdict
data = defaultdict(list)
data['fruits'].append('apple')


# Custom field sort
mylist.sort(key=lambda x: x.foo)

# Regexes
txt = "The rain in Spain"

x = re.search("^The(.*)Spain$", txt)
    'rain in'

x = re.findall("ai", "The rain in Spain")
    ['ai', 'ai']


# Timestamp
from datetime import datetime
now = datetime.now()

dt = datetime.fromisoformat("2024-11-01T09:00:00")

print(now.strftime("%Y-%m-%d %H:%M:%S"))
    '2021-03-07 23:16:41'

dt = datetime.strptime("09/23/2030 8:28","%m/%d/%Y %H:%M")


