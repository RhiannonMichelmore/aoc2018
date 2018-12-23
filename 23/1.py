import os
import math
import sys
import numpy as np
import time
import re
import numpy as np

def solve(filepath):
    bots = []
    regex_string = r'^pos=<(\-?\d+),(\-?\d+),(\-?\d+)>, r=(\d+)$'
    regex = re.compile(regex_string)
    with open(filepath) as f:
        for line in f:
            l = line.strip()
            m = regex.match(l)
            x = int(m.group(1))
            y = int(m.group(2))
            z = int(m.group(3))
            r = int(m.group(4))
            bots.append((x,y,z,r)) 

    s = bots[np.argmax([r for (x,y,z,r) in bots])]
    total = 0
    for idy,c in enumerate(bots):
        m_d = manhat_dist(s[0],s[1],s[2],c[0],c[1],c[2])
        if m_d <= s[3]:
            total += 1

    print(total)

def manhat_dist(x1,y1,z1,x2,y2,z2):
    return abs(x1-x2)+abs(y1-y2)+abs(z1-z2)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
