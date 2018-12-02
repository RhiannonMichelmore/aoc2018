import os
import math
import sys

def solve(filepath):
    twos = 0
    threes = 0
    with open(filepath,'r') as f:
        codes = f.readlines()
        codes = [x.strip() for x in codes]

    for idx,c in enumerate(codes):
        for pos in range(len(c)):
            for idy,cc in enumerate(codes):
                if not idx == idy and not c[pos] == cc[pos] and c[:pos] == cc[:pos] and c[pos+1:] == cc[pos+1:]:
                    print(c[:pos]+c[pos+1:])
                    return

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
