import sys
import re

for fname in sys.argv[1:]:
    print(fname)
    with open(fname, "r") as f:
        lines = f.readlines()

    with open(fname, "w") as f:
        for line in lines:
            m = re.search(r'print (.+)$', line)
            if m and '#' not in line:
                #print(line)
                line = line.rstrip().replace('print ', 'print(') + ')\n'
            m = re.search(r'env python$', line)
            if m:
                line = line.rstrip().replace('env python', 'env python3') + '\n'
            f.write(line)

