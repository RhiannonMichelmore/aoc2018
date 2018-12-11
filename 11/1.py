import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    with open(filepath) as f:
        grid_serial = int(f.readline().strip())

    grid = [[None for x in range(300)] for y in range(300)]

    for y in range(300):
        for x in range(300):
            rack_id = (x+1) + 10
            power_level = rack_id * (y+1)
            power_level += grid_serial
            power_level *= rack_id
            str_pl = str(power_level)
            if len(str_pl) < 3:
                power_level = 0
            else:
                power_level = int(str_pl[-3])
            power_level -= 5
            grid[y][x] = power_level

    max_val = 0
    max_location = None
    for y in range(300-3):
        for x in range(300-3):
            pl = 0
            for j in range(3):
                for i in range(3):
                    pl += grid[y+j][x+i]
            if pl > max_val:
                max_val = pl
                max_location = (x+1,y+1)

    print(max_location)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
