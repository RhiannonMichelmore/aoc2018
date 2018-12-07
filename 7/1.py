import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    dependencies = {}
    counts = {}
    letters = set()
    with open(filepath) as f:
        for line in f:
            parent = line.strip().split(" ")[1]
            child = line.strip().split(" ")[7]
            letters.add(parent)
            letters.add(child)
            if not parent in dependencies:
                dependencies[parent] = [child]
            else:
                dependencies[parent].append(child)
            if not child in counts:
                counts[child] = 1
            else:
                counts[child] += 1
            
    # find root node
    children = []
    for key, val in dependencies.items():
        children = children + val

    children = set(children)

    ordering = ""
    avail_nodes = list(letters.symmetric_difference(children))
    avail_nodes.sort()

    while len(avail_nodes) > 0:
        avail_nodes.sort()
        to_test = avail_nodes.pop(0)
        ordering = ordering + to_test
        if to_test in dependencies:
            children = dependencies[to_test]
            for c in children:
                counts[c] -= 1
                if counts[c] == 0:
                    avail_nodes.append(c)
        avail_nodes = list(set(avail_nodes))

    print(ordering)
    


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
