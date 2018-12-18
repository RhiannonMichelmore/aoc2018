import os
import math
import sys
import numpy as np
import time
import copy

def solve(filepath):
    grid = []
    with open(filepath) as f:
        for line in f:
            to_append = list(line.strip())
            grid.append(to_append)
    x_size = len(grid[0])
    y_size = len(grid)

    minute = 1
    before_grid = grid.copy()
    print("Initial State")
    display(before_grid)
    cycle_recording = []
    print()
    while minute < 10000+1:
        print("Minute",minute)
        after_grid = [[None for x in range(x_size)] for y in range(y_size)]
        for y in range(y_size):
            for x in range(x_size):
                current_value = before_grid[y][x]
                neighbours = get_neighbours((x,y),before_grid)
                if current_value == '.':
                    if neighbours.count('|') >= 3:
                        after_grid[y][x] = '|'
                    else:
                        after_grid[y][x] = '.'
                elif current_value == '|':
                    if neighbours.count('#') >= 3:
                        after_grid[y][x] = '#'
                    else:
                        after_grid[y][x] = '|'
                elif current_value == '#':
                    if neighbours.count('#') >= 1 and neighbours.count('|') >= 1:
                        after_grid[y][x] = '#'
                    else:
                        after_grid[y][x] = '.'
        before_grid = after_grid.copy()

        woods = 0
        lumber_yards = 0
        for y in range(y_size):
            for x in range(x_size):
                if before_grid[y][x] == '|':
                    woods += 1
                elif before_grid[y][x] == '#':
                    lumber_yards += 1
            
        total = woods*lumber_yards
        # probably enough time to converge
        if minute > 1000:
            if len(cycle_recording) == 0:
                cycle_recording.append(total)
            else:
                if total == cycle_recording[0]:
                    # found full cycle!
                    cycle_len = len(cycle_recording)
                    diff = 1000000000-minute
                    mod = diff % cycle_len
                    print(cycle_recording[mod])
                    return
                else:
                    cycle_recording.append(total)
        minute += 1


def get_neighbours(c,gr):
    neighbours = []
    for y in range(-1,2,1):
        for x in range(-1,2,1):
            if not (x==0 and y==0) and not (x==-1 and c[0]==0) and not (x==1 and c[0]==len(gr[0])-1) and not (y==-1 and c[1]==0) and not (y==1 and c[1]==len(gr)-1):
                neighbours.append(gr[c[1]+y][c[0]+x])
    return neighbours


def display(g):
    for y in range(len(g)):
        for x in range(len(g[0])):
            print(g[y][x],end="")
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
