import os
import math
import sys

def solve(filepath):
    value = 0
    with open(filepath,"r") as inputdata:
        for line in inputdata:
            alter = int(line.strip())
            value = value + alter
    print(value)




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
