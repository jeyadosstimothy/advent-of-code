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

min_x = 10**5
max_x = 0
max_y = 0
x_filled = {}
for i, j in filled:
    if(j > max_y):
        max_y = j
    if(i > max_x):
        max_x = i
    if(i < min_x):
        min_x = i

for i, j in filled:
    x_filled[i] = sorted(list(set(x_filled.get(i, []) + [j])))

print(json.dumps(x_filled))

def is_filled(x, y):
    if(y == max_y + 2):
        return True
    return (x, y) in filled

def get_x_filled(x):
    return x_filled.get(x, []) + [max_y + 2]

def update_filled(x, y):
    filled.add((x, y))
    x_filled[x] = sorted(list(set(x_filled.get(x, []) + [y])))

# print(min_x, max_x, max_y)
# print(x_filled)


count = 0

moves = [(0, 1), (-1, 1), (1, 1)]

while(True):
    start_x, start_y = (500, 0)
    stopped = False
    current_move_direction = (0, 1)
    moves_in_direction = 1
    while(True):
        print(count, start_x, start_y)
        idx = bisect.bisect_right(get_x_filled(start_x), start_y)
        new_y = get_x_filled(start_x)[idx] - 1
        if(new_y != start_y and current_move_direction != (0, 1)):
            moves_in_direction = 1
            current_move_direction = (0, 1)
        start_y = new_y
        found_air = False
        next_move_direction = None
        for move in moves:
            temp_x, temp_y = start_x + move[0], start_y + move[1]
            if not is_filled(temp_x, temp_y):
                if found_air:
                    moves_in_direction = 0
                    continue
                next_move_direction = move
                found_air = True
                new_x, new_y = temp_x, temp_y

        if(found_air):
            start_x, start_y = new_x, new_y
        else:
            for i in range(moves_in_direction):
                prev_x, prev_y = start_x - i * current_move_direction[0], start_y - i * current_move_direction[1]
                update_filled(prev_x, prev_y)
            stopped = True
            break
        if(current_move_direction == next_move_direction):
            moves_in_direction = moves_in_direction + 1
        else:
            moves_in_direction = 1
        current_move_direction = next_move_direction
    print(count, start_x, start_y)
    if(stopped and start_y == 0):
        break
    count = count + moves_in_direction

print(count+1)