import os
import math
import sys
import numpy as np

def solve(filepath):
    fabric = np.zeros((1000,1000))
    with open(filepath) as f:
        for line in f:
            parts = line.split(" ")
            locIn, locDown = parts[2][:-1].split(",")
            sizeIn, sizeDown = parts[3].split("x")
            for i in range(int(sizeDown)):
                for j in range(int(sizeIn)):
                    updateLocIn = int(locIn) + j
                    updateLocDown = int(locDown) + i
                    fabric[updateLocDown][updateLocIn] += 1

        count = (fabric > 1).sum()
        print(count)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
