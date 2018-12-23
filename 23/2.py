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
    x_avg, y_avg, z_avg = 0,0,0
    with open(filepath) as f:
        for line in f:
            l = line.strip()
            m = regex.match(l)
            x = int(m.group(1))
            y = int(m.group(2))
            z = int(m.group(3))
            r = int(m.group(4))
            bots.append((x,y,z,r)) 
            x_avg += x
            y_avg += y
            z_avg += z

    x_avg = x_avg/len(bots)
    y_avg = y_avg/len(bots)
    z_avg = z_avg/len(bots)

    bot_totals = []
    for idx,b in enumerate(bots):
        total = 0
        for idy,c in enumerate(bots):
            m_d = manhat_dist(b[0],b[1],b[2],c[0],c[1],c[2])
            if m_d <= b[3]:
                total += 1
        bot_totals.append((b,total))

    bot_totals.sort(key=lambda e: e[1])
    print(bot_totals)

def manhat_dist(x1,y1,z1,x2,y2,z2):
    return abs(x1-x2)+abs(y1-y2)+abs(z1-z2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
