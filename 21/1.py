import os
import math
import sys
import numpy as np
import time
import copy

if __name__ == "__main__":
    val3 = 65536
    val5 = 733884
    val1 = 0
    val0 = 0
    val2 = 0
    values = []
    last = []
    while True:
        val1 = val3 & 255
        val5 = val1 + val5
        val5 = val5 & 16777215
        val5 *= 65899
        val5 = val5 & 16777215

        if 256 > val3:
            if val5 in values:
                pass
            else: 
                values.append(val5)
                print("NO REPEAT",val5)
            if val5 == val0:
                break
            val1 = 0
            val3 = val5 | 65536
            val5 = 733884
        else:
            val1 = int(val3/256)+1
            if (val1*256) > val3:
                val1 -= 1
            if (val1+1)*256 <= val3:
                val1 += 1
            val3 = val1

