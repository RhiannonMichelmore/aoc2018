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

    iterations = 0
    pot_zero = 0
    prev_total = 0
    prev_diff = 0
    same_count = 0
    while True:
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
        if total - prev_total == prev_diff and same_count < 100:
            prev_diff = total - prev_total
            prev_total = total
            same_count += 1
        elif total - prev_total == prev_diff and same_count == 100:
            print(total,prev_total,total-prev_total)
            break
        else:
            same_count = 0
            prev_diff = total - prev_total
            prev_total = total
        iterations += 1

    new_total = total + (50000000000-iterations-1)*prev_diff
    print(new_total)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
