#!/usr/bin/env python3

import argparse
import datetime
import time

from srutils import cmd

ipoints = {
    # Hour: [weekday-vol, weekend-vol]
    0: [4, 4],  #  12am   [x     ]
    1: [4, 4],  #   1am   [x     ]
    2: [3, 3],  #   2am   [x     ]
    3: [2, 2],  #   3am   [x     ]
    4: [2, 2],  #   4am   [xx    ]
    5: [3, 3],  #   5am   [xx    ]
    6: [4, 4],  #   6am   [xxx   ]
    7: [5, 5],  #   7am   [xxx   ]
    8: [5, 5],  #   8am   [xxx   ]
    9: [4, 6],  #   9am   [xx    ]
    10: [0, 5],  # 10am   [      ]
    11: [0, 3],  # 11am   [      ]
    12: [0, 0],  # 12am   [      ]
    13: [0, 0],  #  1pm   [      ]
    14: [0, 0],  #  2pm   [      ]
    15: [0, 0],  #  3pm   [      ]
    16: [0, 0],  #  4pm   [      ]
    17: [0, 0],  #  5pm   [      ]
    18: [0, 0],  #  6pm   [      ]
    19: [0, 0],  #  7pm   [x     ]
    20: [0, 0],  #  8pm   [xx    ]
    21: [0, 0],  #  9pm   [xx    ]
    22: [4, 4],  # 10pm   [xx    ]
    23: [4, 4],  # 11pm   [xx    ]
    24: [4, 4],  # 12am   [xx    ]
}


def get_now():
    # Relies on local
    # maybe pin to EST with dateutil.tz
    return datetime.datetime.now()


def set_vol(v: float):
    # sudo osascript -e "set Volume 0.9"
    # 0-10, accepts floats

    assert v >= 0.0
    assert v <= 10.0

    vnorm = v
    cmd(f'osascript -e "set Volume {vnorm:.1f}"', noisy=True)


def _clamp(x, minn, maxx):
    return max(min(x, maxx), minn)


class Volumizer:
    def __init__(self):
        self.boost = 0.0
        self.updated_at = None
        self.last_degrade = get_now()

    def base_vol(self, t=None):
        """Get the base/scheduled volume without boost"""
        t = t or get_now()

        dow = t.weekday()  # 0 is Mon, 6 is Sun
        weekend = int(dow in (5, 6))

        hour = t.hour
        minute = t.minute
        minutes_perc = float(minute) / 60.0

        cur_h = ipoints[hour][weekend]
        next_h = ipoints[hour + 1][weekend]

        vol = ((1.0 - minutes_perc) * cur_h) + (minutes_perc * next_h)
        return vol

    def get_vol(self, t=None, verbose=False, debug=False):
        """Get the volume with boosting incorporated"""
        t = t or get_now()

        boost_age = (
            ((t - self.updated_at).total_seconds()) if self.updated_at else 1000000
        )

        if boost_age < (2 * 3600):
            boost_perc = 1.0
        elif boost_age < (3 * 3600):
            boost_perc = 1.0 - ((boost_age - (2 * 3600)) / 3600)
        else:
            self.boost = 0.0
            self.updated_at = None
            boost_perc = 0.0
        assert boost_perc >= 0.0 and boost_perc <= 1.0
        base_perc = 1.0 - boost_perc

        base_vol = self.base_vol(t)
        vol = (base_vol * base_perc) + (self.boost * boost_perc)
        vol = _clamp(vol, 0.0, 10.0)
        if debug or verbose:
            # print(f"hour {hour} cur_h {cur_h} next_h {next_h} perc {minutes_perc} vol {vol}")
            boost_str = ""
            if boost_perc > 0.0:
                boost_str = f" [boost={self.boost:.2f} perc={boost_perc:.2f}]"
            debug_str = f"[base vol={base_vol:.2f} perc={base_perc:.2f}] {boost_str}"
            print(f"{t.strftime('%a %I:%M %p')} : vol={vol:.2f} {debug_str}")
            if debug:
                return vol, debug_str

        return vol

    def apply_boost(self, b_delta=None, b_abs=None):
        if b_abs is not None:
            self.boost = b_abs
        if b_delta is not None:
            print(f"Apply boost {self.get_vol()} + {b_delta}")
            self.boost = self.get_vol() + b_delta
        self.boost = _clamp(self.boost, 0.0, 10.0)
        self.updated_at = get_now()
        self.update()

    def unset_boost(self):
        self.updated_at = None
        self.update()

    def update(self):
        t = get_now()
        vol = self.get_vol(t=t, verbose=True)
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
