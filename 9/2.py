import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    with open(filepath) as f:
        l = f.readline().strip().split(" ")
        players = int(l[0])
        marbles = 100*int(l[6])
        
    print("Players:",players,"Marbles:",marbles)

    score = [0 for i in range(players)]
    current_node = Node(0)
    current_node.next = current_node
    current_node.prev = current_node
    current_marble = 1
    current_player = 0
    while current_marble <= marbles+1:
        if current_marble % 23 == 0:
            score[current_player] += current_marble
            current_node = current_node.prev
            current_node = current_node.prev
            current_node = current_node.prev
            current_node = current_node.prev
            current_node = current_node.prev
            current_node = current_node.prev
            current_node = current_node.prev
            score[current_player] += current_node.data
            before = current_node.prev
            after = current_node.next
            before.next = after
            after.prev = before
            current_node = after
        else:
            current_node = current_node.next
            temp = current_node.next
            current_node.next = Node(current_marble)
            current_node.next.prev = current_node
            current_node.next.next = temp
            current_node = current_node.next
            current_node.next.prev = current_node

        current_marble += 1
        if current_player + 1 >= players:
            current_player = 0
        else:
            current_player += 1

    print(max(score))


class Node:
    def __init__(self,data = None):
        self.data = data
        self.next = None
        self.prev = None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
