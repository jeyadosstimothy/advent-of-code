import math
import sys

a_token, b_token = 3, 1

total = 0
lines = sys.stdin.readlines()
while len(lines) != 0:
    # print(lines[:4])
    ax, ay = map(lambda s: int(s.split('+')[1]), lines[0].strip().split(': ')[1].split(', '))
    bx, by = map(lambda s: int(s.split('+')[1]), lines[1].strip().split(': ')[1].split(', '))
    px, py = map(lambda s: int(s.split('=')[1]), lines[2].strip().split(': ')[1].split(', '))
    lines = lines[4:]

    slope_a, slope_b = - (ax / ay), - (bx / by)
    print("Slope:", slope_a, slope_b)

    if slope_a == slope_b:
        continue

    y = (px * ay - ax * py) / (-ax * by + ay * bx )
    x = (py - by * y) / ay
    print("x, y: ", x, y)

    round_x, round_y = math.floor(x), math.floor(y)
    if round_x != x or round_y != y:
        continue

    if x > 100 or y > 100:
        continue

    total = total + a_token * x + b_token * y

print(total)