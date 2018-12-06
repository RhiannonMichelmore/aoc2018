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

    to_consider = coords.copy()
    for y in range(max_y):
        to_remove1 = grid[y][0]
        to_remove2 = grid[y][-1]
        if not to_remove1 == '.' and coords[to_remove1] in to_consider:
            to_consider.remove(coords[to_remove1])
        if not to_remove2 == '.' and coords[to_remove2] in to_consider:
            to_consider.remove(coords[to_remove2])

    for x in range(max_x):
        to_remove1 = grid[0][x]
        to_remove2 = grid[-1][x]
        if not to_remove1 == '.' and coords[to_remove1] in to_consider:
            to_consider.remove(coords[to_remove1])
        if not to_remove2 == '.' and coords[to_remove2] in to_consider:
            to_consider.remove(coords[to_remove2])

    max_spaces = 0
    for c in to_consider:
        count = sum(xs.count(coords.index(c)) for xs in grid)
        if count > max_spaces:
            max_spaces = count

    print(max_spaces)


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
