import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    points = []
    vels = []
    with open(filepath) as f:
        for line in f:
            cut = line.strip().split("<")
            position = [int(cut[1].split(">")[0].split(",")[0].strip()),int(cut[1].split(">")[0].split(",")[1].strip())]
            velocity = [int(cut[2].split(">")[0].split(",")[0].strip()),int(cut[2].split(">")[0].split(",")[1].strip())]
            points.append(position)
            vels.append(velocity)

    orig_points = points[:]
    orig_vels = vels[:]

    xs = [p[0] for p in points]
    min_x = min(xs)
    max_x = max(xs)
    ys = [p[1] for p in points]
    min_y = min(ys)
    max_y = max(ys)
    bounding_box_area = (max_x-min_x)*(max_y-min_y)
    print(bounding_box_area)

    found = False
    count = 0
    while not found:
        change = False
        if bounding_box_area < 1000:
            display(points)
        for idx,p in enumerate(points):
            updatex = p[0] + vels[idx][0]
            updatey = p[1] + vels[idx][1]
            p[0] = updatex
            p[1] = updatey
        new_area = get_bounded_area(points)
        if new_area > bounding_box_area:
            found = True
            print("Iteration of word:",count)
        bounding_box_area = new_area
        print(bounding_box_area)
        count += 1


def get_bounded_area(points_list):
    xs = [p[0] for p in points_list]
    min_x = min(xs)
    max_x = max(xs)
    ys = [p[1] for p in points_list]
    min_y = min(ys)
    max_y = max(ys)
    return (max_x-min_x)*(max_y-min_y)

def display(points_list):
    xs = [p[0] for p in points_list]
    min_x = min(xs)
    max_x = max(xs)
    ys = [p[1] for p in points_list]
    min_y = min(ys)
    max_y = max(ys)
    grid = [['_' for i in range(max_x-min_x+1)] for j in range(max_y-min_y+1)]
    for p in points_list:
        grid[p[1]-min_y][p[0]-min_x] = '#'

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            print(grid[y][x],end="")
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
