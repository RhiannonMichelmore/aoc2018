import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    maze = []
    carts = []
    with open(filepath) as f:
        y = 0
        for line in f:
            if line[-1] == '\n':
                row = list(line[:-1])
            else:
                row = list(line)
            for idx, c in enumerate(row):
                if c == '^':
                    cart = Minecart(idx,y,'N')
                    carts.append(cart)
                    row[idx] = '|'
                elif c == '>':
                    cart = Minecart(idx,y,'E')
                    carts.append(cart)
                    row[idx] = '-'
                elif c == 'v':
                    cart = Minecart(idx,y,'S')
                    carts.append(cart)
                    row[idx] = '|'
                elif c == '<':
                    cart = Minecart(idx,y,'W')
                    carts.append(cart)
                    row[idx] = '-'
            maze.append(row)
            y += 1

    carts.sort(key=lambda x: (x.y,x.x))
    while True:
        carts.sort(key=lambda x: (x.y,x.x))
        # Movement
        for cart in carts:
            if cart.facing == 'N':
                cart.y -= 1
            elif cart.facing == 'E':
                cart.x += 1
            elif cart.facing == 'S':
                cart.y += 1
            else:
                cart.x -= 1
            cart.facing = turn(maze,cart)
            carts = remove_colliding(carts)
        if len(carts) == 1:
            print(carts[0].x,carts[0].y,carts[0].facing)
            return

def remove_colliding(cs):
    carts = [c for idx, c in enumerate(cs) if collide(idx,c,cs) == False]
    return carts

def collide(idx,c,cs):
    for idy,cn in enumerate(cs):
        if not idy == idx:
            if cn.x == c.x and cn.y == c.y:
                return True
    return False

def turn(maze,cart):
    if maze[cart.y][cart.x] == '/':
        if cart.facing == 'N':
            return 'E'
        elif cart.facing == 'W':
            return 'S'
        elif cart.facing == 'S':
            return 'W'
        elif cart.facing == 'E':
            return 'N'
    elif maze[cart.y][cart.x] == '\\':
        if cart.facing == 'N':
            return 'W'
        elif cart.facing == 'W':
            return 'N'
        elif cart.facing == 'S':
            return 'E'
        elif cart.facing == 'E':
            return 'S'
    elif maze[cart.y][cart.x] == '+':
        f = decide(cart.facing, cart.turning) 
        cart.update_turn()
        return f
    else:
        return cart.facing

def decide(facing,turn):
    if facing == 'N':
        if turn == 'l':
            return 'W'
        elif turn == 'r':
            return 'E'
    elif facing == 'E':
        if turn == 'l':
            return 'N'
        elif turn == 'r':
            return 'S'
    elif facing == 'S':
        if turn == 'l':
            return 'E'
        elif turn == 'r':
            return 'W'
    elif facing == 'W':
        if turn == 'l':
            return 'S'
        elif turn == 'r':
            return 'N'
    return facing

class Minecart:
    def __init__(self,x,y,facing):
        self.x = x
        self.y =y
        self.facing = facing
        self.turning = 'l'
    def update_turn(self):
        if self.turning == 'l':
            self.turning = 's'
        elif self.turning == 's':
            self.turning = 'r'
        else:
            self.turning = 'l'

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
