import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    rules = {}
    with open(filepath) as f:
        state = f.readline().strip().split(" ")[2]
        f.readline()
        for l in f.readlines():
            rule = l.strip()
            left = rule.split(" ")[0]
            right = rule.split(" ")[2]
            rules[left] = right

    pot_zero = 0
    iterations = 0
    while iterations < 20:
        index = 2
        diff = len(state) - len(state.lstrip('.'))
        pot_zero += 5 - diff
        state = state.lstrip('.').rstrip('.')
        state = "....." + state + "....."
        new_state = list(state[:])
        total = 0
        while index < len(state)-2:
            to_check = state[index-2:index+3]
            if to_check in rules:
                char = rules[to_check]
                new_state[index] = char
                if char == '#':
                    total += index-pot_zero
            else:
                new_state[index] = '.'
            index += 1
        state = "".join(new_state)
        iterations += 1

    print(total)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
