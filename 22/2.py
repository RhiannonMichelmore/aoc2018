import os
import math
import sys
import numpy as np
import time
import collections

def solve(filepath):
    with open(filepath) as f:
        depth = int(f.readline().strip().split(" ")[1])
        targetx, targety = [int(x) for x in f.readline().strip().split(" ")[1].split(",")]
    print(depth,targetx, targety)
    size_modx = 200
    size_mody = 200
    cave = [[None for x in range(targetx+1+size_modx)] for y in range(targety+1+size_mody)]
    tool_grid = [[None for x in range(targetx+1+size_modx)] for y in range(targety+1+size_mody)]
    max_to_zero = (8*(targetx+targety))+7

    for y in range(len(cave)):
        for x in range(len(cave[0])):
            if x == targetx and y == targety:
                gi = 0
            elif x==0 and y==0:
                gi = 0
            elif y == 0:
                gi = x*16807
            elif x == 0:
                gi = y*48271
            else:
                gi = cave[y][x-1]*cave[y-1][x]
            el = (gi + depth) % 20183
            cave[y][x] = el
            terrain = el % 3
            if terrain == 0:
                tool_grid[y][x] = 'neither'
            elif terrain == 1:
                tool_grid[y][x] = 'torch'
            else:
                tool_grid[y][x] = 'climbing'

    directions = [(-1,0),(0,-1),(1,0),(0,1)]
    tools = ['neither','torch','climbing']

    time_grid = [[{'torch':None,'neither':None,'climbing':None} for x in range(targetx+1+size_modx)] for y in range(targety+1+size_mody)]
    time_grid[targety][targetx]['torch'] = 0

    to_explore = collections.deque()
    to_explore.append((targetx,targety,'torch',0))
    counter = -1
    while len(to_explore) > 0:
        counter += 1
        x,y,tool,prev_time = to_explore.popleft()
        current_time = time_grid[y][x][tool]
        if prev_time > current_time:
            continue
        if current_time + ((x + y)*8)+7 < max_to_zero:
            max_to_zero = current_time + ((x+y)*8)+7
        if current_time + x + y > max_to_zero:
            continue

        for direction in directions:
            posx = x + direction[0]
            posy = y + direction[1]
            if posx >= 0 and posx < len(cave[0]) and posy >= 0 and posy < len(cave):
                # check if the tool can actually be used to move on
                if not tool == tool_grid[posy][posx]:
                    new_time = time_grid[y][x][tool] + 1
                    if time_grid[posy][posx][tool] == None or time_grid[posy][posx][tool] > new_time:
                        time_grid[posy][posx][tool] = new_time
                        to_explore.append((posx,posy,tool,new_time))

        for new_tool in tools:
            if not new_tool == tool:
                if not new_tool == tool_grid[y][x]:
                    new_time = time_grid[y][x][tool] + 7
                    if time_grid[y][x][new_tool] == None or time_grid[y][x][new_tool] > new_time:
                        time_grid[y][x][new_tool] = new_time
                        to_explore.append((x,y,new_tool,new_time))

    print(time_grid[0][0]['torch'])




#def (cave,x,y,dx,dy,time_grid,to_explore,tool):


def display_grid_dist(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            l = len(str(grid[y][x]))
            print((" "*(3-l)) + str(grid[y][x]) + " ",end="")
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)

