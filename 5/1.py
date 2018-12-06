import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    with open(filepath) as f:
        line = f.readline().strip()

    print(line)
    done = False
    while not done:
        done = True
        curr_char = line[0]
        for idx, char in enumerate(line):
            if not idx == 0:
                if opposite(char) == curr_char:
                    line = line[:idx-1] + line[idx+1:]
                    done = False
                    break
                else:
                    curr_char = char


    print(line)
    print(len(line))


def opposite(char):
    if char.islower():
        return char.upper()
    if char.isupper():
        return char.lower()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
