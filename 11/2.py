import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    with open(filepath) as f:
        grid_serial = int(f.readline().strip())

    grid = [[0 for x in range(300)] for y in range(300)]

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
    max_size = 0
    calcs = []
    for size in range(1,300):
        new_calcs = [[0 for x in range(300-(size-1))] for y in range(300-(size-1))]
        print(size)
        for y in range(300-(size-1)):
            for x in range(300-(size-1)):
                if size > 1:
                    pl = calcs[-1][y][x]
                    #add new column on right
                    for j in range(size):
                        pl += grid[y+j][x+(size-1)]
                    #add new row on bottom BUT IGNORE CORNER SO WE DONT DOUBLE ADD
                    for i in range(size-1):
                        pl += grid[y+(size-1)][x+i]
                else:
                    pl = grid[y][x]

                new_calcs[y][x] = pl
                if pl > max_val:
                    max_val = pl
                    max_location = (x+1,y+1)
                    max_size = size
        calcs.append(new_calcs)

    print(max_location,max_size)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
