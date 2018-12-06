import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    with open(filepath) as f:
        line = f.readline().strip()

    i = 0
    while True:
        curr_char = line[i]
        rest = line[i+1:]
        if len(rest) == 0:
            break
        if rest[0].upper() == curr_char or rest[0].lower() == curr_char

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
