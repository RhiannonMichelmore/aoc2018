import os
import math
import sys
import numpy as np
import time
import re
import numpy as np
import networkx as nx

def solve(filepath):
    G=nx.Graph()
    points = []
    with open(filepath) as f:
        for line in f:
            coords = line.strip().split(",")
            curr_coord = (int(coords[0]),int(coords[1]),int(coords[2]),int(coords[3]))
            points.append(curr_coord)
            G.add_node(curr_coord)
            for node in G.nodes():
                if md(node,curr_coord) <= 3:
                    G.add_edge(node,curr_coord)

    print(nx.number_connected_components(G))


def md(j,k):
    return abs(j[0]-k[0]) + abs(j[1]-k[1]) + abs(j[2]-k[2]) + abs(j[3]-k[3])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
