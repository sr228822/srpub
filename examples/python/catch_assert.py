#!/usr/bin/env python

import sys
import traceback

try:
    assert 7 == 1
except AssertionError as e:
    s = traceback.format_exc()
    print 'lol assert did fail {}'.format(s)
    print 'lol assert message {}'.format(sys.exc_info()[0])

print 'im still alive'
