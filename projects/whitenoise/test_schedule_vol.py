#!/usr/bin/env python3

import datetime
import time

from schedule_vol import get_vol, set_vol, _update

def test_interp():
    fake_time = datetime.datetime.now()
    while True:
        _update(fake_time)
        fake_time = fake_time + datetime.timedelta(minutes=5)
        time.sleep(0.1)

if __name__ == "__main__":
    test_interp()
