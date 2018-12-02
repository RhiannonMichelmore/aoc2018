import os
import math
import sys
from collections import Counter

def solve(filepath):
    twos = 0
    threes = 0
    with open(filepath,'r') as f:
        for line in f:
            counts = Counter(line.strip())
            twos = twos + (1 if len([1 for (a,b) in counts.most_common() if b == 2]) >= 1 else 0)
            threes = threes + (1 if len([1 for (a,b) in counts.most_common() if b == 3]) >= 1 else 0)
        print(twos*threes)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
