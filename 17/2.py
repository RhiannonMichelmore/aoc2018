import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    min_x = 1000000
    max_x = 0
    min_y = 1000000
    max_y = 0
    with open(filepath) as f:
        for line in f:
            cut = line.strip().split(",")
            if cut[0][0] == 'x':
                x_val = int(cut[0][2:])
                if x_val < min_x:
                    min_x = x_val
                if x_val > max_x:
                    max_x = x_val
            else:
                y_val =  int(cut[0][2:])
                if y_val < min_y:
                    min_y = y_val
                if y_val > max_y:
                    max_y = y_val
                
            if cut[1][1] == 'x':
                x_val_min = int(cut[1].split("..")[0][3:])
                x_val_max = int(cut[1].split("..")[1])
                if x_val_min < min_x:
                    min_x = x_val_min
                if x_val_max > max_x:
                    max_x = x_val_max
            else:
                y_val_min = int(cut[1].split("..")[0][3:])
                y_val_max = int(cut[1].split("..")[1])
                if y_val_min < min_y:
                    min_y = y_val_min
                if y_val_max > max_y:
                    max_y = y_val_max

    print("X range:",min_x,max_x)
    print("Y range:",min_y,max_y)
    print()
    min_x -= 2
    max_x += 2
    max_y += 2

    grid = [["." for x in range((max_x+1)-min_x)] for y in range(max_y+1)]
    grid[0][(500-min_x)] = '+'

    with open(filepath) as fi:
        for line in fi:
            cut = line.strip().split(",")
            if cut[0][0] == 'x':
                x_val = int(cut[0][2:])
                y_val_min = int(cut[1].split("..")[0][3:])
                y_val_max = int(cut[1].split("..")[1])
                for it in range((y_val_max+1)-y_val_min):
                    grid[y_val_min+it][x_val-min_x] = '#'
            else:
                y_val =  int(cut[0][2:])
                x_val_min = int(cut[1].split("..")[0][3:])
                x_val_max = int(cut[1].split("..")[1])
                for it in range((x_val_max+1)-x_val_min):
                    grid[y_val][(x_val_min-min_x)+it] = '#'


    grid[1][500-min_x] = '|'
    flowing = [(500-min_x,1)]
    while len(flowing) > 0:
        current = flowing.pop(-1)
        if current[1] >= max_y-1:
            continue
        if grid[current[1]+1][current[0]] == '.':
            grid[current[1]+1][current[0]] = '|'
            flowing.append(current)
            flowing.append((current[0],current[1]+1))
        elif grid[current[1]+1][current[0]] == '#' or grid[current[1]+1][current[0]] == '~':
            #scan left and right to see if its contained
            contained = True
            scanning_left = True
            curr_coord = (current[0],current[1])
            left_edge = None
            while scanning_left:
                if not grid[curr_coord[1]+1][curr_coord[0]] == '#' and not grid[curr_coord[1]+1][curr_coord[0]] == '~':
                    scanning_left = False
                    contained = False
                    left_edge = curr_coord
                elif grid[curr_coord[1]][curr_coord[0]-1] == '#':
                    contained = True
                    scanning_left = False
                    left_edge = curr_coord
                curr_coord = (curr_coord[0]-1,curr_coord[1])
            scanning_right = True
            right_edge = None
            curr_coord = (current[0],current[1])
            while scanning_right:
                if not grid[curr_coord[1]+1][curr_coord[0]] == '#' and not grid[curr_coord[1]+1][curr_coord[0]] == '~':
                    scanning_right = False
                    contained = False
                    right_edge = curr_coord
                elif grid[curr_coord[1]][curr_coord[0]+1] == '#':
                    if contained == True:
                        contained = True
                    scanning_right = False
                    right_edge = curr_coord
                curr_coord = (curr_coord[0]+1,curr_coord[1])

            if contained:
                for xx in range(left_edge[0],right_edge[0]+1):
                    grid[left_edge[1]][xx] = '~'
            else:
                for xx in range(left_edge[0],right_edge[0]+1):
                    grid[left_edge[1]][xx] = '|'
                if grid[left_edge[1]+1][left_edge[0]] == '.':
                    flowing.append(left_edge)
                if grid[right_edge[1]+1][right_edge[0]] == '.':
                    flowing.append(right_edge)


    total = 0
    for y in range(min_y,max_y-1):
        for x in range(len(grid[0])):
            if grid[y][x] == '~':
                total += 1

    print(total)

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
