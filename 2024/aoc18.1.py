import sys

directions = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

def turn(direction, offset):
    s = '^>v<'
    new = (s.find(direction) + offset) % 4
    return s[new]

def get_next(i, j, direction):
    di, dj = directions[direction]
    return i + di, j + dj

def within_bounds(i, j, bounds):
    return i >= 0 and j >= 0 and i < bounds[0] and j < bounds[1]

if __name__ == '__main__':
    bounds = tuple(map(int, sys.stdin.readline().strip().split(',')))
    sys.stdin.readline()
    corruption_incoming = [tuple(map(int, line.strip().split(','))) for line in sys.stdin]
    corrupted = set(corruption_incoming[:1024])

    start = (0, 0)
    end = (bounds[0] - 1, bounds[1] - 1)

    visited = set()
    visited.add(start)
    queue = [(*start, 0)]
    steps_to_end = None
    while len(queue) != 0:
        i, j, steps = queue[0]
        queue = queue[1:]
        if (i, j) == end:
            steps_to_end = steps
            break
        for d in directions:
            ni, nj = get_next(i, j, d)
            if within_bounds(ni, nj, bounds) and (ni, nj) not in corrupted and (ni, nj) not in visited:
                visited.add((ni, nj))
                queue.append((ni, nj, steps + 1))
    print(steps_to_end)
