''' EightPuzzleWithManhattan.py
by Khoa Tran
UWNetID: ktdt01
Student number: 1861460

An instance of Manhattan distance heuristic.
'''

from EightPuzzle import *

def h(self):
    sum = 0
    yList = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    xList = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    for x in range(3):
        for y in range(3):
            value = self.b[x][y]
            if value != 0:
                xPoint = xList[value]
                yPoint = yList[value]
                xDiff = abs(x - xPoint)
                yDiff = abs(y - yPoint)
                sum += (xDiff + yDiff)
    return sum




