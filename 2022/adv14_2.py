import sys
import bisect
import json

filled = set()

for line in sys.stdin:
    points = [[int(x) for x in point.split(',')] for point in line.strip().split(' -> ')]

    for i in range(len(points) - 1):
        x1, y1, x2, y2 = points[i][0], points[i][1], points[i+1][0], points[i+1][1]
        if(y1 == y2):
            for j in range(min(x1, x2), max(x1, x2)+1):
                filled.add((j, y1))
        if(x1 == x2):
            for j in range(min(y1, y2), max(y1, y2)+1):
                filled.add((x1, j))

max_y = 0
for i, j in filled:
    if(j > max_y):
        max_y = j

moves = [(0, 1), (-1, 1), (1, 1)]
current_row = [(500, 0)]
count = len(current_row)

for i in range(1, max_y + 2):
    new_row = set()
    for point in current_row:
        for move in moves:
            print(point, move)
            new_point = (point[0] + move[0], point[1] + move[1])
            if(new_point not in filled):
                new_row.add(new_point)
    current_row = list(new_row)
    count = count + len(current_row)

print(count)