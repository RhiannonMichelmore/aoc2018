import os
import math
import sys
import numpy as np
import time

def solve(filepath):
    with open(filepath) as f:
        entries = f.readlines()
    entries = [x.strip() for x in entries]
    entries.sort(key = lambda x: time.mktime(time.strptime(x.split("]")[0][1:],'%Y-%m-%d %H:%M')))

    days = []
    guards = []
    for idx, i in enumerate(entries):
        d = i[1:11]
        if d not in days:
            days.append(d)
        if i[19] == 'G' and i[26:30].split(' ')[0] not in guards:
            guards.append(i[26:30].split(' ')[0])

    num_days = len(days)
    num_guards = len(guards)
    
    records = np.zeros((num_days,num_guards,60))
    records_by_guard = np.zeros((num_guards,num_days,60))
    
    curr_guard = 0
    guard_idx = -1
    sleep_start = 0
    sleep_end = 0
    for e in entries:
        if e[19] == 'G':
            curr_guard = e[26:30].split(' ')[0]
            guard_idx = guards.index(curr_guard)
        else:
            day_str = e[1:11]
            day_idx = days.index(day_str)
            if e[19] == 'f':
                sleep_start = int(e[15:17])
            elif e[19] == 'w':
                sleep_end = int(e[15:17])
                records[day_idx][guard_idx][sleep_start:sleep_end] = 1
                records_by_guard[guard_idx][day_idx][sleep_start:sleep_end] = 1 

    # (occurance, minute)
    max_minute_per_guard = []
    for g in range(num_guards):
        to_consider = records_by_guard[g]
        to_consider_flat = np.sum(to_consider,axis=0)
        min_most = np.argmax(to_consider_flat)
        min_most_occurance = max(to_consider_flat)
        max_minute_per_guard.append((min_most_occurance,min_most))

    #get max
    high_occurance = 0
    high_guard = -1
    high_min = -1
    for idx, entry in enumerate(max_minute_per_guard):
        if entry[0] > high_occurance:
            high_occurance = entry[0]
            high_guard = idx
            high_min = entry[1]

    print(int(guards[high_guard])*high_min)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
