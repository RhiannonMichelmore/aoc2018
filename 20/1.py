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

    backup = sys.stdout

    sys.stdout = StringIO()
    re.compile(regex,re.DEBUG)
    out = sys.stdout.getvalue()

    sys.stdout.close()
    sys.stdout = backup

    print(out)
    branching_map = [0 for i in range(out.count("SUBPATTERN"))]
    split = out.split("\n")
    print(split)
    create_tree(regex[1:-1],Node("",None))
    
def create_tree(regex,root):
    position = 0
    curr_string = ""
    while position < len(regex):
        if is_literal(regex[position]):
            curr_string = curr_string + regex[position]
        elif regex[position] == '(':
            child = Node(curr_string,None)
            # get until matching )
            stack = ['(']
            p = position + 1
            while True:
                if regex[p] == ')':
                    if stack[-1] == '(':
                        stack.pop(-1)
                        if len(stack) == 0:
                            break
                    else:
                        stack.append(')')
                if regex[p] == '(':
                    if stack[-1] == ')':
                        stack.pop(-1)
                        if len(stack) == 0:
                            break
                    else:
                        stack.append('(')
                p += 1
            new_reg = regex[position:p+1]
            # now get branches
            branches = get_branches(new_reg[1:-1])
            branch_trees = [create_tree(b,child) for b in branches]
            sys.exit(0)

        position += 1

def get_leaves(root):
    leaves = []
    if root.children == []:
        return [root]
    else:
        for child in root.children:
            leaves = leaves + get_leaves(child)
    return leaves

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
    
class Node:
    def __init__(self,string,parent):
        self.string = string
        self.parent = parent
        self.children = []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
