''' EightPuzzleWithHamming.py
by Khoa Tran
UWNetID: ktdt01
Student number: 1861460

An instance of hamming distance heuristic.
'''

from EightPuzzle import *

def h(self):   
    count = 0
    value = 0
    for x in range(3):
        for y in range(3):
            state = self.b[x][y]
            if value == 0:
                value = 1
            else:
                if state != value:
                    count += 1
                value += 1
    return count

