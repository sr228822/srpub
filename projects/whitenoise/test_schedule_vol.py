#!/usr/bin/env python3

import datetime
import time

from schedule_vol import get_vol, set_vol

def test_interp():
    fake_time = datetime.datetime.now()
    while True:
        vol = get_vol(fake_time)
        print(f"{fake_time.strftime('%I:%M %p')}: {vol:.2f}")
        fake_time = fake_time + datetime.timedelta(minutes=5)
        time.sleep(0.1)
        set_vol(vol)

if __name__ == "__main__":
    test_interp()
