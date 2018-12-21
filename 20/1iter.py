import os
import math
import sys
import numpy as np
import time
import copy
import re
from io import StringIO
import glob

def solve(filepath):
    with open(filepath) as f:
        regex = f.readline().strip()
    root = Node("",regex[1:-1])
    to_expand = [root]
    while len(to_expand) > 0:
        node = to_expand.pop(-1)
        curr_child_string = ""
        curr_child_exp = ""
        position = 0
        while position < len(node.exp):
            if is_literal(node.exp[position]) or node.exp[position]=='|':
                curr_child_string += node.exp[position]
            elif node.exp[position] == '(':
                # get until matching )
                stack = ['(']
                p = position + 1
                while True:
                    if node.exp[p] == ')':
                        if stack[-1] == '(':
                            stack.pop(-1)
                            if len(stack) == 0:
                                break
                        else:
                            stack.append(')')
                    if node.exp[p] == '(':
                        if stack[-1] == ')':
                            stack.pop(-1)
                            if len(stack) == 0:
                                break
                        else:
                            stack.append('(')
                    p += 1
                curr_child_exp = node.exp[position+1:p]
                position = p
                branches = get_branches(curr_child_exp)
                for b in branches:
                    #print(curr_child_string,b)
                    new_node = Node(curr_child_string,b)
                    node.children.append(new_node)
                    to_expand.append(new_node)
                curr_child_string = ""
                curr_child_exp = ""
            position += 1
        if position == len(node.exp) and not curr_child_string == "":
            node.children.append(Node(curr_child_string,""))
    for c in root.children:
        print(c.string, c.exp)
    print("DISP")
    display_tree(root,0)
    print("-----")
    strings = gen_strings_iter(root)
    print("----")

def display_tree(root,level):
    print(level, root.string, root.exp, len(root.children))
    if not len(root.children) == 0:
        for c in root.children:
            display_tree(c,level+1)

def gen_strings(r):
    strings = []
    print(r.string)
    if len(r.children) == 0:
        return [r.string]
    else:
        for c in r.children:
            child_strings = gen_strings(c)
            print(child_strings)
            for child in child_strings:
                strings.append(r.string+child)
        return strings

def gen_strings_iter(r):
    strings = []
    to_visit = [r]
    decisions = []
    while len(to_visit) > 0:
        visiting = to_visit.pop(-1)
        if not len(visiting.children) == 0:
            decisions.append(len(visiting.children))
            for c in visiting.children:
                to_visit.append(c)
    print(decisions)
    new_visiting = [r]
    while len(new_visiting) >0:
        v = new_visiting.pop(-1)
        print(v.string)
        if len(v.children) >0:
            new_visiting.append(v.children[0])

    return []

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
    def __init__(self,string,exp):
        self.string = string
        self.exp = exp
        self.branches = []
        self.children = []
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
