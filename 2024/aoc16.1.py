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

def print_graph(graph):
    for row in graph:
        print(''.join(row))
    print()

if __name__ == '__main__':
    
    graph = [list(line.strip()) for line in sys.stdin]
    si, sj = None, None
    ei, ej = None, None
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] == 'S':
                si, sj = i, j
            if graph[i][j] == 'E':
                ei, ej = i, j

    costs = [[None for _ in row] for row in graph]
    queue = [(si, sj, 0, '>')]

    while len(queue) != 0:
        i, j, cost, direction = queue[0]
        queue = queue[1:]
        if costs[i][j] is not None and cost >= costs[i][j]:
            continue
        costs[i][j] = cost
        turns = [0, -1, 1, 2]
        for offset in turns:
            new_direction = turn(direction, offset)
            ni, nj = get_next(i, j, new_direction)
            if graph[ni][nj] == '#':
                continue
            queue.append((ni, nj, cost + abs(1000 * offset) + 1, new_direction))
    
    print(costs[ei][ej])


# 302116
# 159564