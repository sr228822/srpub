#!/usr/bin/python

import sys, traceback
for threadId, stack in sys._current_frames().items():
    print "\n# ThreadID: %s" % threadId
    for filename, lineno, name, line in traceback.extract_stack(stack):
        print 'File: "%s", line %d, in %s' % (filename, lineno, name)
        if line:
            print "  %s" % (line.strip())
