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
    0:  [0.4, 0.4], # 12am   [xx    ]
    1:  [0.4, 0.4], #  1am   [xx    ]
    2:  [0.3, 0.3], #  2am   [x     ]
    3:  [0.3, 0.3], #  3am   [x     ]
    4:  [0.3, 0.3], #  4am   [x     ]
    5:  [0.4, 0.4], #  5am   [xx    ]
    6:  [0.5, 0.5], #  6am   [xxx   ]
    7:  [0.6, 0.6], #  7am   [xxxx  ]
    8:  [0.6, 0.6], #  8am   [xxxx  ]
    9:  [0.5, 0.6], #  9am   [xxx   ]
    10: [OFF, 0.5], # 10am   [      ]
    11: [OFF, 0.3], # 11am   [      ]
    12: [OFF, OFF], # 12am   [      ]
    13: [OFF, OFF], #  1pm   [      ]
    14: [OFF, OFF], #  2pm   [      ]
    15: [OFF, OFF], #  3pm   [      ]
    16: [OFF, OFF], #  4pm   [      ]
    17: [OFF, OFF], #  5pm   [      ]
    18: [OFF, OFF], #  6pm   [      ]
    19: [OFF, OFF], #  7pm   [      ]
    20: [OFF, OFF], #  8pm   [      ]
    21: [OFF, OFF], #  9pm   [      ]
    22: [0.4, 0.4], # 10pm   [xx    ]
    23: [0.4, 0.4], # 11pm   [xx    ]
    24: [0.4, 0.4], # 12am   [xx    ]
}


def get_now():
    # Relies on local
    # maybe pin to EST with dateutil.tz
    return datetime.datetime.now()

def set_vol(v: float):
    #sudo osascript -e "set Volume 0.9"
    # 0-10, accepts floats

    assert v >= 0.0
    assert v <= 1.0

    vnorm = v * 10.0
    cmd(f'osascript -e "set Volume {vnorm:.1f}"', noisy=True)

def get_vol(t):
    dow = t.weekday()  # 0 is Mon, 6 is Sun
    weekend = int(dow in (5, 6))

    hour = t.hour
    minute = t.minute
    minutes_perc = float(minute) / 60.0

    cur_h = ipoints[hour][weekend]
    next_h = ipoints[hour+1][weekend]

    vol = ((1.0 - minutes_perc) * cur_h) + (minutes_perc * next_h)
    #print(f"hour {hour} cur_h {cur_h} next_h {next_h} perc {minutes_perc} vol {vol}")
    return vol

def print_status(t, vol):
    print(f"{t.strftime('%a %I:%M %p')}: {vol:.2f}")

def _update(t):
    vol = get_vol(t)
    print_status(t, vol)
    set_vol(vol)

def main(interval=120):
    while True:
        _update(get_now())
        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("white noise vol control")
    parser.add_argument(
        '--interval',
        type=int,
        required=False,
        default=5,
        help='Eval interval in minutes')
    args = parser.parse_args()
    main(interval=(args.interval * 60))
