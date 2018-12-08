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

    avail_nodes = list(letters.symmetric_difference(children))
    avail_nodes.sort()
    letters = list(letters)
    letters.sort()

    n_workers = 5 #4 for final
    time_offset = 60 #60 for final
    workers = [Worker() for n in range(n_workers)]

    second = -1
    finished_nodes = 0

    while finished_nodes < len(letters):
        # finish any current tasks that need finishing
        for w in workers:
            if w.busy == True:
                w.time_elapsed += 1
                if w.time_elapsed == w.time_expected:
                    w.time_elapsed = 0
                    w.time_expected = 0
                    w.busy = False
                    done_node = w.node
                    finished_nodes += 1
                    w.node = ''
                    if done_node in dependencies:
                        children = dependencies[done_node]
                        for c in children:
                            counts[c] -= 1
                            if counts[c] == 0:
                                avail_nodes.append(c)

        free_workers = [w for w in workers if w.busy == False]
        avail_nodes.sort()
        for fw in free_workers:
            if len(avail_nodes) > 0:
                assign_node = avail_nodes.pop(0)
                fw.busy = True
                fw.node = assign_node
                fw.time_expected = time_offset + letters.index(assign_node) + 1

        second += 1

    print(second)

class Worker:
    def __init__(self):
        self.busy = False
        self.node = ''
        self.time_elapsed = 0
        self.time_expected = 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
