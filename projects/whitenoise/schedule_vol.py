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
    0: MED,   # 12am   [xxx   ]
    1: LOW,   #  1am   [x     ]
    2: LOW,   #  2am   [x     ]
    3: LOW,   #  3am   [x     ]
    4: LOW,   #  4am   [x     ]
    5: LOW,   #  5am   [x     ]
    6: MED,   #  6am   [xxx   ]
    7: HIGH,  #  7am   [xxxxx ]
    8: HIGH,  #  8am   [xxxxx ]
    9: MED,   #  9am   [xxx   ]
    10: OFF,  # 10am   [      ]
    11: OFF,  # 11am   [      ]
    12: OFF,  # 12am   [      ]
    13: OFF,  #  1pm   [      ]
    14: OFF,  #  2pm   [      ]
    15: OFF,  #  3pm   [      ]
    16: OFF,  #  4pm   [      ]
    17: OFF,  #  5pm   [      ]
    18: OFF,  #  6pm   [      ]
    19: OFF,  #  7pm   [      ]
    20: OFF,  #  8pm   [      ]
    21: LOW,  #  9pm   [x     ]
    22: MED,  # 10pm   [xxx   ]
    23: MED,  # 11pm   [xxx   ]
    24: MED,  # 12am   [xxx   ]
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
    #weekday = t.weekday()  # 0 is Mon, 6 is Sun
    #is_weekend = weekday in (5, 6)

    hour = t.hour
    minute = t.minute
    minutes_perc = float(minute) / 60.0

    cur_h = ipoints[hour]
    next_h = ipoints[hour+1]

    vol = ((1.0 - minutes_perc) * cur_h) + (minutes_perc * next_h)
    #print(f"hour {hour} cur_h {cur_h} next_h {next_h} perc {minutes_perc} vol {vol}")
    return vol


def main(interval=120):
    while True:
        now = get_now()
        vol = get_vol(now)
        print(f"{now.strftime('%I:%M %p')}: {vol:.2f}")
        set_vol(vol)
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
