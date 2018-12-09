import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    with open(filepath) as f:
        l = f.readline().strip().split(" ")
        players = int(l[0])
        #marbles = 100*int(l[6])
        marbles = int(l[6])
        
    print("Players:",players,"Marbles:",marbles)

    score = [0 for i in range(players)]
    game_list = [0]
    current_idx = 0
    current_marble = 1
    current_player = 0
    while current_marble <= marbles+1:
        if current_marble % 23 == 0:
            score[current_player] += current_marble
            index = get_index('counter',7,game_list,current_idx)
            additional = game_list.pop(index)
            score[current_player] += additional
            print(current_marble+additional)
            if index >= len(game_list):
                current_idx = 0
            else:
                current_idx = index
        else:
            index = get_index('clock',1,game_list,current_idx)
            if index + 1 == len(game_list):
                game_list.append(current_marble)
                current_idx = index + 1
            else:
                game_list.insert(index+1,current_marble)
                current_idx = index + 1
        current_marble += 1
        if current_player + 1 >= len(score):
            current_player = 0
        else:
            current_player += 1

    print(max(score))

def get_index(direction,spaces,glist,curridx):
    if direction == 'counter':
        idx = curridx
        for i in range(spaces):
            if idx - 1 < 0:
                idx = len(glist) - 1
            else:
                idx -= 1
        return idx

    elif direction == 'clock':
        idx = curridx
        for i in range(spaces):
            if idx + 1 >= len(glist):
                idx = 0
            else:
                idx += 1
        return idx
    else:
        print("Not a valid direction.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
