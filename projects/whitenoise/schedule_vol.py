#!/usr/bin/env python3

import argparse
import datetime
import time

from srutils import cmd

OFF = 0.0
LOW = 0.3
MED = 0.5
HIGH = 0.7
MAX = 1.0

ipoints = {
    # Hour: [weekday-vol, weekend-vol]
    0: [0.4, 0.4],  #  12am   [xx    ]
    1: [0.4, 0.4],  #   1am   [xx    ]
    2: [0.3, 0.3],  #   2am   [x     ]
    3: [0.3, 0.3],  #   3am   [x     ]
    4: [0.3, 0.3],  #   4am   [x     ]
    5: [0.4, 0.4],  #   5am   [xx    ]
    6: [0.5, 0.5],  #   6am   [xxx   ]
    7: [0.6, 0.6],  #   7am   [xxxx  ]
    8: [0.6, 0.6],  #   8am   [xxxx  ]
    9: [0.5, 0.6],  #   9am   [xxx   ]
    10: [OFF, 0.5],  # 10am   [      ]
    11: [OFF, 0.3],  # 11am   [      ]
    12: [OFF, OFF],  # 12am   [      ]
    13: [OFF, OFF],  #  1pm   [      ]
    14: [OFF, OFF],  #  2pm   [      ]
    15: [OFF, OFF],  #  3pm   [      ]
    16: [OFF, OFF],  #  4pm   [      ]
    17: [OFF, OFF],  #  5pm   [      ]
    18: [OFF, OFF],  #  6pm   [      ]
    19: [OFF, OFF],  #  7pm   [      ]
    20: [OFF, OFF],  #  8pm   [      ]
    21: [OFF, OFF],  #  9pm   [      ]
    22: [0.4, 0.4],  # 10pm   [xx    ]
    23: [0.4, 0.4],  # 11pm   [xx    ]
    24: [0.4, 0.4],  # 12am   [xx    ]
}


def get_now():
    # Relies on local
    # maybe pin to EST with dateutil.tz
    return datetime.datetime.now()


def set_vol(v: float):
    # sudo osascript -e "set Volume 0.9"
    # 0-10, accepts floats

    assert v >= 0.0
    assert v <= 1.0

    vnorm = v * 10.0
    cmd(f'osascript -e "set Volume {vnorm:.1f}"', noisy=True)


def _clamp(x, minn, maxx):
    return max(min(x, maxx), minn)


class Volumizer:
    def __init__(self):
        self.boost = 0.0
        self.updated_at = None
        self.last_degrade = get_now()

    def degrade_boost(self):
        if not self.updated_at:
            return

        now = get_now()
        age = (now - self.updated_at).total_seconds()

        # leave as is for 2 hours
        if age < (2 * 3600):
            return

        # this can be called frequently so only degrade every 3 mins
        if (now - self.last_degrade).total_seconds() < 3 * 60:
            return
        self.last_degrade = now

        # then ramp back to baseline (0 boost)
        self.boost = (self.boost - 0.02) * 0.95
        if self.boost < 0.01:
            self.boost = 0.0
            self.updated_at = None

    def get_vol(self, t):
        dow = t.weekday()  # 0 is Mon, 6 is Sun
        weekend = int(dow in (5, 6))

        hour = t.hour
        minute = t.minute
        minutes_perc = float(minute) / 60.0

        cur_h = ipoints[hour][weekend]
        next_h = ipoints[hour + 1][weekend]

        vol = ((1.0 - minutes_perc) * cur_h) + (minutes_perc * next_h)

        self.degrade_boost()
        vol = _clamp((vol + (self.boost / 10.0)), 0.0, 1.0)
        # print(f"hour {hour} cur_h {cur_h} next_h {next_h} perc {minutes_perc} vol {vol}")
        return vol

    def apply_boost(self, b_delta=None, b_abs=None):
        if b_abs is not None:
            self.boost = b_abs
        if b_delta is not None:
            self.boost += b_delta
        self.updated_at = get_now()
        self.update()

    def print_status(self, t, vol):
        boost_str = ""
        if self.boost != 0.0:
            age = int((get_now() - self.updated_at).total_seconds())
            boost_str = f" [Boost {self.boost:.2f} age {age}] "
        print(f"{t.strftime('%a %I:%M %p')}: {boost_str}{vol:.2f}")

    def update(self):
        t = get_now()
        vol = self.get_vol(t)
        self.print_status(t, vol)
        set_vol(vol)


def main(interval=120):
    v = Volumizer()
    while True:
        v.update()
        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("white noise vol control")
    parser.add_argument(
        "--interval",
        type=int,
        required=False,
        default=5,
        help="Eval interval in minutes",
    )
    args = parser.parse_args()
    main(interval=(args.interval * 60))
