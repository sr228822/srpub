from collections import defaultdict, namedtuple

Point = namedtuple("Point", ["timestamp", "value"])


class SimpleTimeMap:
    def __init__(self):
        self.data = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        # Stores key, value pair at the given timestamp
        self.data[key].append(Point(timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        # Returns value of key at the given timestamp, or "" if none exists
        # If multiple values exist, return the value with largest timestamp less than or equal to the query timestamp

        points = self.data.get(key)
        if not points:
            return ""

        # sort by timestamp
        # not necessary if set calls always come in order
        # points.sort(key=lambda x: x.timestamp)

        for point in points:
            if point.timestamp < timestamp:
                continue
            return point.value
        return ""


class TimeMap:
    def __init__(self):
        self.data = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        # Stores key, value pair at the given timestamp
        self.data[key].append(Point(timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        # Returns value of key at the given timestamp, or "" if none exists
        # If multiple values exist, return the value with largest timestamp less than or equal to the query timestamp

        points = self.data.get(key)
        if not points:
            return ""

        # sort by timestamp
        # not necessary if set calls always come in order
        # points.sort(key=lambda x: x.timestamp)

        # Find timestamp using a binary search for log-N performance
        bottom = 0
        top = len(points) - 1

        while True:
            print(f"bottom={bottom} top={top} timestamp={timestamp} points={points}")
            if top == bottom:
                if points[bottom].timestamp > timestamp:
                    # all points are above the time
                    return ""
                return points[bottom].value
            if top - bottom <= 1:
                # bottom=0 top=1 timestamp=4 points=[Point(timestamp=1, value='bar'), Point(timestamp=4, value='bar2')]
                if points[bottom].timestamp > timestamp:
                    # all points are above the time
                    return ""
                elif (
                    points[bottom].timestamp <= timestamp
                    and points[top].timestamp > timestamp
                ):
                    return points[bottom].value
                elif points[top].timestamp >= timestamp:
                    return points[top].value
                if points[top].timestamp > timestamp:
                    return points[top].value
                break

            half = int((top - bottom) / 2) + bottom
            point = points[half]
            if point.timestamp > timestamp:
                top = half
            elif point.timestamp < timestamp:
                bottom = half
            else:
                # exact match
                return point.value


def test_timestamp_basic():
    store = TimeMap()

    # set foo-> bar at time 1
    store.set("foo", "bar", 1)  # store "bar" at timestamp 1
    assert store.get("foo", 1) == "bar"  # returns "bar"
    assert store.get("foo", 3) == "bar"  # returns "bar" (last value before timestamp 3)

    # set a new value at time 4
    store.set("foo", "bar2", 4)  # store "bar2" at timestamp 4
    assert store.get("foo", 4) == "bar2"  # returns "bar2"
    assert store.get("foo", 2) == "bar"  # returns "bar" (last value before timestamp 2)
    assert store.get("foo", 0) == ""  # returns "" (no values before timestamp 0)


def test_timestamp_edges():
    store = TimeMap()
    assert store.get("asdf", 0) == ""


def test_floats():
    store = TimeMap()
    store.set("foo", "bar1", 1)
    store.set("foo", "bar2", 2)
    store.get("foo", 1.5)  # Should return "bar1"


def test_overwrite():
    store = TimeMap()
    store.set("foo", "bar", 4)  # store "bar2" at timestamp 4
    store.set("foo", "bar2", 4)  # store "bar2" at timestamp 4
    assert store.get("foo", 4) == "bar2"  # returns "bar2"
