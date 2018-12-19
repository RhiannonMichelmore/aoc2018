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

    registers = [0,0,0,0,0,0]
    last_state = []
    counter = 0
    used = False
    skipped = 0
    while registers[instr_reg] < len(lines):
        instr = lines[registers[instr_reg]]

        #print("ip=" + str(registers[instr_reg]) +(" "*(7-len(str(registers[instr_reg]))))+ " [",end="")
        '''
        for idx,r in enumerate(registers):
            if idx < len(registers)-1:
                print(str(r) + ", ",end="")
            else:
                print(str(r) + "] ",end="")
        '''

        #print(instr.name + " " + str(instr.a) + " " + str(instr.b) + " " + str(instr.c) + " [",end="")
        registers[instr.c] = functions[instr.name](instr.a,instr.b,registers)
        '''
        if (registers[instr_reg] == 2 and used == False):
            used = True
            registers[instr.c] = 10551403
        elif (registers[instr_reg] == 2 and used == True):
            skipped += 1
        '''

        '''
        if skipped > 4:
            used = True
        for idx,r in enumerate(registers):
            if idx < len(registers)-1:
                print(str(r) + (" "*(9-len(str(r)))) +", ",end="")
            else:
                print(str(r) + (" "*(9-len(str(r)))) + "] ",end="")
        print()
        '''

        last_state = registers[:]
        registers[instr_reg] += 1
        #if counter > 300:
        #    break
        counter += 1

    print(last_state[0])
    print("ip=" + str(registers[instr_reg]))

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
