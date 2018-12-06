import os
import math
import sys
import numpy as np
import time
import re

def solve(filepath):
    with open(filepath) as f:
        line = f.readline().strip()

    print(line)
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    min_len = 10000000

    for a in alphabet:
        print(a)
        replaced_line = re.sub(a,'',line)
        replaced_line = re.sub(a.upper(),'',replaced_line)
        print()
        done = False
        while not done:
            done = True
            curr_char = replaced_line[0]
            for idx, char in enumerate(replaced_line):
                if not idx == 0:
                    if opposite(char) == curr_char:
                        replaced_line = replaced_line[:idx-1] + replaced_line[idx+1:]
                        done = False
                        break
                    else:
                        curr_char = char
        length = len(replaced_line)
        if length < min_len:
            min_len = length
    print(min_len)



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
