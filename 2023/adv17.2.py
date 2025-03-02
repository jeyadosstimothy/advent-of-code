import sys
import heapq

def read_grid():
    grid = []
    for line in sys.stdin:
        grid.append(list(map(int, line.strip())))
    return grid

def print_grid(grid):
    for line in grid:
        print(''.join(map(str, line)))
    print()

def move(i, j, d):
    directions = {
        '^': (-1, 0),
        '<': (0, -1),
        'v': (1, 0),
        '>': (0, 1)
    }
    di, dj = directions[d]
    return i + di, j + dj

def turn(d, o):
    directions = '>^<v'
    return directions[(directions.find(d) + o) % 4]

def traverse(grid):
    visited = {}
    queue = []
    heapq.heappush(queue, (-grid[0][0], 0, 0, '>', 0, []))
    heapq.heappush(queue, (-grid[0][0], 0, 0, 'v', 0, []))

    while len(queue) != 0:
        h, i, j, d, s, p = heapq.heappop(queue)
        if (i, j, d, s) in visited:
            continue
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
            continue
        h = h + grid[i][j]
        visited[(i, j, d, s)] = h
        # p.append((i, j, d))

        if s >= 4:
            if i == len(grid) - 1 and j == len(grid[0]) - 1:
                return h, p
            heapq.heappush(queue, (h, *move(i, j, turn(d, 1)), turn(d, 1), 1, list(p)))
            heapq.heappush(queue, (h, *move(i, j, turn(d, -1)), turn(d, -1), 1, list(p)))
        if s < 10:
            heapq.heappush(queue, (h, *move(i, j, d), d, s + 1, list(p)))
    raise Exception('Unexpected')

grid = read_grid()
# print_grid(grid)
h, p = traverse(grid)
print(h)
for pp in p:
    print(pp)