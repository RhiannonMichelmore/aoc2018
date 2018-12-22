import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    with open(filepath) as f:
        depth = int(f.readline().strip().split(" ")[1])
        targetx, targety = [int(x) for x in f.readline().strip().split(" ")[1].split(",")]
    print(depth,targetx, targety)
    grid = [[None for x in range(targetx+1)] for y in range(targety+1)]
    total = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if x == targetx and y == targety:
                gi = 0
            elif x==0 and y==0:
                gi = 0
            elif y == 0:
                gi = x*16807
            elif x == 0:
                gi = y*48271
            else:
                gi = grid[y][x-1]*grid[y-1][x]
            el = (gi + depth) % 20183
            if el % 3 == 1:
                total += 1
            elif el % 3 == 2:
                total += 2
            grid[y][x] = el

    print(total)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
