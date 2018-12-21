import os
import math
import sys
import numpy as np
import time
import copy
import re
from io import StringIO

def solve(filepath):
    with open(filepath) as f:
        regex = f.readline().strip()
    strings = []
    strings = gen_strings(regex[1:-1])
    print(strings)

def gen_strings(regex):
    strings = []
    position = 0
    curr_string = ""
    # if its just a string
    if sum([1 for x in regex if is_literal(x)]) == len(regex):
        return [regex]
    else:
        found_branch = False
        tmp_strings = []
        while not found_branch:
            if is_literal(regex[position]):
                curr_string += regex[position]
            elif regex[position] == '(':
                # get until matching )
                stack = ['(']
                p = position + 1
                while True:
                    if regex[p] == ')':
                        if stack[-1] == '(':
                            stack.pop(-1)
                            if len(stack) == 0:
                                found_branch = True
                                break
                        else:
                            stack.append(')')
                    if regex[p] == '(':
                        if stack[-1] == ')':
                            stack.pop(-1)
                            if len(stack) == 0:
                                found_branch = True
                                break
                        else:
                            stack.append('(')
                    p += 1
                new_reg = regex[position:p+1]
                # get branches here
                branches = get_branches(new_reg[1:-1])
                for b in branches:
                    tmp_strings = tmp_strings + gen_strings(b)
                if not curr_string == "":
                    for i in range(len(tmp_strings)):
                        tmp_strings[i] = curr_string + tmp_strings[i]
            position += 1
        tail_strings = gen_strings(regex[p+1:])
        all_strings = []
        for tmp in tmp_strings:
            for tail in tail_strings:
                new_string = tmp+tail
                all_strings.append(new_string)
        return all_strings

def get_branches(regex):
    position = 0
    branches = []
    stack = []
    curr_string = ""
    while position < len(regex):
        if is_literal(regex[position]):
            curr_string += regex[position]
        elif regex[position] == ')':
            curr_string += regex[position]
            if len(stack) > 0 and stack[-1] == '(':
                stack.pop(-1)
            else:
                stack.append(')')
        elif regex[position] == '(':
            curr_string += regex[position]
            if len(stack) > 0 and stack[-1] == ')':
                stack.pop(-1)
            else:
                stack.append('(')
        elif regex[position] == '|' and len(stack) == 0:
            branches.append(curr_string)
            curr_string = ""
        elif regex[position] == '|' and len(stack) > 0:
            curr_string += regex[position]
        position += 1
    if not curr_string == "":
        branches.append(curr_string)
    if regex[-1] == '|':
        branches.append("")
    return branches


def is_literal(c):
    if c == 'N' or c == 'W' or c == 'S' or c == 'E':
        return True
    else:
        return False

if __name__ == "__main__":
    sys.setrecursionlimit(10000000)
    print(sys.getrecursionlimit())
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
