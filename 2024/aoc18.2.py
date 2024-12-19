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

    start = (0, 0)
    end = (bounds[0] - 1, bounds[1] - 1)

    lower, upper = 0, len(corruption_incoming)
    while lower != upper:
        fallen = (lower + upper) // 2
        corrupted_list = corruption_incoming[:fallen]
        corrupted = set(corrupted_list)

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

        # print(fallen)
        # for j in range(bounds[1]):
        #     row = ''
        #     for i in range(bounds[0]):
        #         if (i, j) in corrupted:
        #             row = row + '#'
        #         elif (i, j) in visited:
        #             row = row + 'O'
        #         else:
        #             row = row + '.'
        #     print(row)
        # print()
        print(lower, upper, fallen, steps_to_end)
        if steps_to_end is None:
            upper = fallen
        else:
            lower = fallen + 1

    print(corruption_incoming[lower - 1])
