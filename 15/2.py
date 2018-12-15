import os
import copy
import math
import sys
import numpy as np
import time

def solve(filepath):
    grid = []
    units = []
    with open(filepath) as f:
        for idy, line in enumerate(f):
            current = list(line.strip())
            for idx, c in enumerate(current):
                if c == 'G':
                    units.append(Unit(idx,idy,c,3))
                elif c == 'E':
                    units.append(Unit(idx,idy,c,4))
            grid.append(current)

    units.sort(key=lambda u: (u.y,u.x))

    '''
    g = shortest_path_grid(grid,1,1)
    for yy in range(len(g)):
        for xx in range(len(g[0])):
            if g[yy][xx] == None:
                print(grid[yy][xx],end="")
            else:
                print(len(g[yy][xx]),end="")
        print()
    '''

    found = False
    attack = 4
    while not found:
        print(attack)
        for u in units:
            if u.faction == 'E':
                u.attack = attack
        found = solve_grid(copy.deepcopy(grid),copy.deepcopy(units))
        attack += 1


def solve_grid(gr,un):
    rn = 0
    while True:
        un.sort(key=lambda u: (u.y,u.x))
        i = 0
        while i < len(un):
            unit = un[i]
            unit_spg = shortest_path_grid(gr,unit.x,unit.y)
            #Move
            targets = [u for u in un if not u.faction == unit.faction]
            if len(targets) == 0:
                display(gr)
                print("All dead.")
                print(rn)
                sumhp = sum([uu.hp for uu in un])
                print(sumhp)
                print(rn*sumhp)
                return True
            target_squares = []
            for t in targets:
                if not unit_spg[t.y][t.x-1] == None:
                    target_squares.append([t.x-1,t.y,unit_spg[t.y][t.x-1]])
                if not unit_spg[t.y][t.x+1] == None:
                    target_squares.append([t.x+1,t.y,unit_spg[t.y][t.x+1]])
                if not unit_spg[t.y-1][t.x] == None:
                    target_squares.append([t.x,t.y-1,unit_spg[t.y-1][t.x]])
                if not unit_spg[t.y+1][t.x] == None:
                    target_squares.append([t.x,t.y+1,unit_spg[t.y+1][t.x]])

            target_squares.sort(key=lambda t: (len(t[2]),t[1],t[0]))
            if not len(target_squares) == 0:
                destination = target_squares[0]
                if len(destination[2]) == 1:
                    gr[unit.y][unit.x] = '.'
                    unit.x = destination[0]
                    unit.y = destination[1]
                    gr[unit.y][unit.x] = unit.faction
                elif len(destination[2]) > 1:
                    gr[unit.y][unit.x] = '.'
                    unit.x = destination[2][1][0]
                    unit.y = destination[2][1][1]
                    gr[unit.y][unit.x] = unit.faction

            to_attack = [t for t in targets if (t.x == unit.x and t.y == unit.y-1) or (t.x == unit.x and t.y == unit.y+1) or (t.x == unit.x-1 and t.y ==unit.y) or (t.x == unit.x+1 and t.y == unit.y)]
            if not len(to_attack) == 0:
                to_attack.sort(key=lambda t: (t.hp,t.y,t.x))
                victim = to_attack[0]
                victim.hp -= unit.attack
                if victim.hp <= 0:
                    if victim.faction == 'E':
                        return False
                    gr[victim.y][victim.x] = '.'
                    ind = un.index(victim)
                    if ind < i:
                        i -= 1
                    un.remove(victim)
            i += 1

        rn += 1

def shortest_path_grid(grid,x,y):
    distance_grid = [[None for i in range(len(grid[0]))] for j in range(len(grid))]
    distance_grid[y][x] = []
    to_search = [(x,y)]
    while len(to_search) > 0:
        expand = to_search.pop(0)
        if grid[expand[1]-1][expand[0]] == '.' and distance_grid[expand[1]-1][expand[0]] == None:
            distance_grid[expand[1]-1][expand[0]] = distance_grid[expand[1]][expand[0]] + [expand]
            to_search.append((expand[0],expand[1]-1))
        if grid[expand[1]][expand[0]-1] == '.' and distance_grid[expand[1]][expand[0]-1] == None:
            distance_grid[expand[1]][expand[0]-1] = distance_grid[expand[1]][expand[0]] + [expand]
            to_search.append((expand[0]-1,expand[1]))
        if grid[expand[1]][expand[0]+1] == '.' and distance_grid[expand[1]][expand[0]+1] == None:
            distance_grid[expand[1]][expand[0]+1] = distance_grid[expand[1]][expand[0]] + [expand]
            to_search.append((expand[0]+1,expand[1]))
        if grid[expand[1]+1][expand[0]] == '.' and distance_grid[expand[1]+1][expand[0]] == None:
            distance_grid[expand[1]+1][expand[0]] = distance_grid[expand[1]][expand[0]] + [expand]
            to_search.append((expand[0],expand[1]+1))
    return distance_grid

def display(g):
    for y in range(len(g)):
        for x in range(len(g[0])):
            print(g[y][x], end="")
        print()
def display_dist_grid(grid,g):
    for yy in range(len(g)):
        for xx in range(len(g[0])):
            if g[yy][xx] == None:
                print(grid[yy][xx],end="")
            else:
                print(len(g[yy][xx]),end="")
        print()

def list_units(u):
    for unit in u:
        print(unit.faction, "X:",unit.x,"Y:",unit.y)

class Unit:
    def __init__(self,x,y,faction,attack):
        self.x = x
        self.y = y
        self.hp = 200
        self.faction = faction
        self.attack = attack

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
