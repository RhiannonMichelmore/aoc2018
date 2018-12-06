import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    coords = []
    with open(filepath) as f:
        for line in f:
            x,y = line.strip().split(" ")
            x = x[:-1]
            coords.append((int(x),int(y)))

    max_x = max([i[0] for i in coords]) + 2
    max_y = max([i[1] for i in coords]) + 2

    grid = [['.' for x in range(max_x)] for y in range(max_y)]

    for y in range(max_y):
        for x in range(max_x):
            min_dist = 1000000
            min_coord = (-1,-1)
            dists = []
            cs = []
            equal = False
            for c in coords:
                dist = manhat_dist(x,y,c[0],c[1])
                dists.append(dist)
            #get min dist index and value
            min_dist = min(dists)
            if dists.count(min_dist) > 1:
                equal = True
            else:
                min_coord = coords[dists.index(min_dist)]

            if equal == False:
                letter = coords.index(min_coord)
                grid[y][x] = letter
            else:
                grid[y][x] = '.'

    zone_coords = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            dist = 0
            for c in coords:
                mh = manhat_dist(x,y,c[0],c[1])
                dist += mh
            if dist < 10000:
                zone_coords.append((x,y))

    print(len(zone_coords))


def manhat_dist(x1,y1,x2,y2):
    return abs(x1-x2) + abs(y1-y2)

def display(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            print(grid[y][x],end='')
        print()
            
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
