import os
import math
import sys
import numpy as np
import time
import copy
import sys
from io import StringIO
import re

def solve(filepath):
    with open(filepath) as f:
        regex = f.readline().strip()

    grid_size = 1000
    limit_dist = 1000

    start_location = (int(grid_size/2),int(grid_size/2))
    grid = [[GridEntry() for x in range(grid_size)] for y in range(grid_size)]
    grid[start_location[1]][start_location[0]].distance = 0

    index = 0
    # stack of (index_in_regex,player_location_when_got_to_that_index,starting_dist,index_in_max_map)
    branch_stack = []

    directions = {'N':(0,-1),'W':(-1,0),'S':(0,1),'E':(1,0)}
    player_location = start_location
    min_x = grid_size
    min_y = grid_size
    max_x = 0
    max_y = 0
    max_dist = 0
    counter = 0
    dist_numbers = {}
    map_dist_numbers = {}
    over_thousand = 0
    while True:
        '''
        if counter % 50000 == 0:
            grid_copy = trim_grid(grid,min_x,min_y,max_x,max_y)
            display_grid(grid_copy,(0,0))
        '''
        char = regex[index]
        #print(branch_stack,index,char)
        if char == '$':
            if len(branch_stack) == 0:
                break

            #print(branch_stack[-1][0])
            branch_stack, player_location, index = next_branch(branch_stack,grid,player_location,regex)
            #print(index)
        elif char in directions:
            movement = directions[char]
            grid[player_location[1]][player_location[0]].doors[char] = True
            dist = grid[player_location[1]][player_location[0]].distance
            player_location = (player_location[0] + movement[0], player_location[1] + movement[1])
            grid[player_location[1]][player_location[0]].doors[get_op(char)] = True
            if player_location[0] < min_x:
                min_x = player_location[0]
                if min_x < 0:
                    print("OUTSIDE GRID")
            if player_location[0] > max_x:
                max_x = player_location[0]
                if max_x >= grid_size:
                    print("OUTSIDE GRID")
            if player_location[1] < min_y:
                min_y = player_location[1]
                if min_y < 0:
                    print("OUTSIDE GRID")
            if player_location[1] > max_y:
                max_y = player_location[1]
                if max_y >= grid_size:
                    print("OUTSIDE GRID")

            if grid[player_location[1]][player_location[0]].distance == None:
                grid[player_location[1]][player_location[0]].distance = dist + 1
                if grid[player_location[1]][player_location[0]].distance >= limit_dist:
                    over_thousand += 1
            else:
                if len(branch_stack) == 0:
                    break
                original = grid[player_location[1]][player_location[0]].distance
                branch_stack, player_location, index = next_branch(branch_stack,grid,player_location,regex)


        elif char == '(':
            #print(index,[k for k,v in map_dist_numbers.items()])
            if index in map_dist_numbers:
                print("short circuit")
                if len(branch_stack) == 0:
                    break
                branch_stack, player_location, index = next_branch(branch_stack,grid,player_location,regex)
            else:
                branch_stack.append((index,player_location,grid[player_location[1]][player_location[0]].distance,index))
                map_dist_numbers[index] = {}
        elif char == '|':
            index = next_closing_bracket(regex,index)
        index += 1
        counter += 1

    #grid = trim_grid(grid,min_x,min_y,max_x,max_y)
    new_start_location = (start_location[0]-min_x,start_location[1]-min_y)
    #display_grid(grid,new_start_location)
    print(over_thousand)
    print("X:",min_x,max_x)
    print("Y:",min_y,max_y)

def next_branch(branch_stack,grid,player_location,regex):
    last_frame = branch_stack.pop(-1)
    last_location = last_frame[1]
    last_index = last_frame[0]
    #print(last_index)
    last_start_dist = last_frame[2]
    map_index = last_frame[3]
    
    player_location = last_location
    index = next_pipe_or_closing(regex,last_index)

    if regex[index] == '|':
        branch_stack.append((index,player_location,last_start_dist,map_index))

    return branch_stack,player_location,index

def next_closing_bracket(regex,index):
    counter = 0
    ind = index
    while True:
        ind += 1
        if regex[ind] == ')' and counter == 0:
            return ind
        elif regex[ind] == ')':
            counter -= 1
        elif regex[ind] == '(':
            counter += 1
def next_pipe_or_closing(regex,index):
    counter = 0
    ind = index
    while True:
        ind += 1
        if (regex[ind] == '|' or regex[ind] == ')') and counter == 0:
            return ind
        elif regex[ind] == ')':
            counter -= 1
        elif regex[ind] == '(':
            counter += 1

def trim_grid(grid,min_x,min_y,max_x,max_y):
    g = grid[min_y:max_y+1]
    new = []
    for row in g:
        new.append(row[min_x:max_x+1])
    return new

def display_grid(grid,start_location):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x].doors['N'] == True:
                print("#--",end="")
            else:
                print("###",end="")
        print("#")
        for x in range(len(grid[0])):
            if grid[y][x].doors['W'] == True:
                print("|",end="")
            else:
                print("#",end="")
            if y == start_location[1] and x == start_location[0]:
                print(" X",end="")
            else:
                #print("  ",end="")
                if not grid[y][x].distance == None:
                    padding = 2-len(str(grid[y][x].distance))
                    print((" "*padding)+str(grid[y][x].distance),end="")
                else:
                    print("  ",end="")
        print("#")
    print("#"*((len(grid)*3)+1))

def is_literal(c):
    if c == 'W' or c == 'N' or c == 'E' or c == 'S':
        return True
    else:
        return False

def get_op(d):
    if d == 'N':
        return 'S'
    elif d == 'W':
        return 'E'
    elif d == 'S':
        return 'N'
    elif d == 'E':
        return 'W'

class GridEntry:
    def __init__(self):
        self.doors = {'N':False,'S':False,'E':False,'W':False}
        self.distance = None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
    '''
    backup = sys.stdout
    sys.stdout = StringIO()     # capture output
    re.compile(regex,re.DEBUG)
    out = sys.stdout.getvalue() # release output
    sys.stdout.close()  # close the stream 
    sys.stdout = backup # restore original stdout
    print(out)
    '''
