import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    with open(filepath) as f:
        recipes = int(f.readline().strip())
    f1 = Node(None,None,3)
    f2 = Node(f1,f1,7)
    f1.prev = f2
    f1.next = f2

    length = 2
    start = f1
    end = f2
    elf1 = f1
    elf2 = f2
    while length <= recipes + 10:
        result = elf1.data + elf2.data
        for c in str(result):
            length += 1
            end.next = Node(end,None,int(c))
            end = end.next
        end.next = start
        move1 = elf1.data + 1
        move2 = elf2.data + 1
        for i in range(move1):
            elf1 = elf1.next
        for i in range(move2):
            elf2 = elf2.next
        #print_list(start,end)

    current = start
    for i in range(recipes):
        current = current.next

    score = ""
    for i in range(10):
        score += str(current.data)
        current = current.next

    print(score)



def print_list(start,end):
    current = start
    while not current == end:
        print(str(current.data)+ " ",end="")
        current = current.next
    print(end.data)

class Node:
    def __init__(self, p, n, data):
        self.prev = p
        self.next = n
        self.data = data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
