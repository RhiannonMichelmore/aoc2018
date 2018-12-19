import os
import math
import sys
import numpy as np
import time
import copy

def solve(filepath):
    functions = {}
    functions['addr'] = lambda a,b,regs: regs[a] + regs[b]
    functions['addi'] = lambda a,b,regs: regs[a] + b
    functions['mulr'] = lambda a,b,regs: regs[a] * regs[b]
    functions['muli'] = lambda a,b,regs: regs[a] * b
    functions['banr'] = lambda a,b,regs: regs[a] & regs[b]
    functions['bani'] = lambda a,b,regs: regs[a] & b
    functions['borr'] = lambda a,b,regs: regs[a] | regs[b]
    functions['bori'] = lambda a,b,regs: regs[a] | b
    functions['setr'] = lambda a,b,regs: regs[a]
    functions['seti'] = lambda a,b,regs: a
    functions['gtir'] = lambda a,b,regs: 1 if a > regs[b] else 0
    functions['gtri'] = lambda a,b,regs: 1 if regs[a] > b else 0
    functions['gtrr'] = lambda a,b,regs: 1 if regs[a] > regs[b] else 0
    functions['eqir'] = lambda a,b,regs: 1 if a == regs[b] else 0
    functions['eqri'] = lambda a,b,regs: 1 if regs[a] == b else 0
    functions['eqrr'] = lambda a,b,regs: 1 if regs[a] == regs[b] else 0

    instr_reg = -1
    lines = []
    with open(filepath) as f:
        instr_reg = int(f.readline().strip().split(" ")[1])
        for line in f:
            l = line.strip().split()
            i = instruction(l[0],int(l[1]), int(l[2]), int(l[3]))
            lines.append(i)

    # after hours of working it out, this code produces the sum of factors of whatever the big value turns out to be =.=

    #registers = [0,4,10551403,1,10551403,10551403]
    #registers = [1,8,10551403,2,0,10551404]
    #registers = [1,8,10551403,3,0,10551404]
    #registers = [1,4,10551403,19,10551403,555337]
    #registers = [20,4,10551403,555337,10551403,19]
    #registers = [555357,4,10551403,10551403,10551403,1]
    #registers = [11106760,8,10551403,10551403,0,10551404]
    registers = [1,0,0,0,0,0]
    last_state = []
    count = 0
    while registers[instr_reg] < len(lines):
        instr = lines[registers[instr_reg]]
        registers[instr.c] = functions[instr.name](instr.a,instr.b,registers)
        last_state = registers[:]
        if count > 30:
            break
        registers[instr_reg] += 1
        count += 1

    number = max(registers)
    factors = [1,number]
    factors = factors + all_factors(number)
    print(factors)
    print(sum(factors))

def all_factors(n):
    factors = []
    i = 2
    while i <(n/2)+1:
        if n%i == 0:
            factors.append(i)
        i+=1
    return factors

class instruction:
    def __init__(self,name,a,b,c):
        self.name = name
        self.a = a
        self.b = b
        self.c = c
    def __repr__(self):
        return "(Instr: " + self.name + ", A: " + str(self.a) + ", B: " + str(self.b) + ", C: " + str(self.c) + ")"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)

