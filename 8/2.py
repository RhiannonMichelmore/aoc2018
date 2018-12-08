import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    with open(filepath) as f:
        line = f.readline().strip()

    numbers = line.split(" ")
    tree = construct(numbers)
    print(node_value(tree))

def node_value(node):
    if len(node.children) == 0:
        return sum(node.metadata)
    else:
        val = 0
        for e in node.metadata:
            if e <= len(node.children) and e > 0:
                val += node_value(node.children[e-1])
        return val

def construct(numbers):
    n_children = int(numbers.pop(0))
    n_meta = int(numbers.pop(0))
    children = []
    for i in range(n_children):
        children.append(construct(numbers))

    meta = []
    for i in range(n_meta):
        meta.append(int(numbers.pop(0)))

    return Node(children,meta)
                
class Node:
    def __init__(self,c,m):
        self.children = c
        self.metadata = m

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
