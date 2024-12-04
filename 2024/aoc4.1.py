import sys

def get_next(curr):
    to_find = 'XMAS'
    return to_find[to_find.find(curr) + 1]

def within_bounds(graph, i, j):
    return i>=0 and j >=0 and i < len(graph) and j < len(graph[0])

def get_num_matches(graph, i, j):
    if graph[i][j] != 'X':
        raise Exception('Not X')

    matches = 0
    directions = {
        'up': (-1, 0),
        'up right': (-1, 1),
        'right': (0, 1),
        'down right': (1, 1),
        'down': (1, 0),
        'down left': (1, -1),
        'left': (0, -1),
        'up left': (-1, -1)
    }
    for direction in directions:
        xmas = 'X'
        di, dj = i, j
        for _ in range(3):
            di, dj = di + directions[direction][0], dj + directions[direction][1]
            if not within_bounds(graph, di, dj):
                break
            xmas = xmas + graph[di][dj]
        if xmas == 'XMAS':
            matches = matches + 1
    return matches

def print_graph(graph):
    for row in graph:
        print(row)

if __name__ == '__main__':
    graph = [list(line.strip()) for line in sys.stdin]
    print_graph(graph)

    x_locations = []
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j] == 'X':
                x_locations.append((i, j))

    total = 0
    while len(x_locations) != 0:
        i, j = x_locations[0]
        total = total + get_num_matches(graph, i, j)
        x_locations = x_locations[1:]

    print(total)
