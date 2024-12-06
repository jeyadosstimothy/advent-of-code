import sys

def get_next(curr):
    to_find = '^>v<'
    return to_find[(to_find.find(curr) + 1)%4]

def within_bounds(graph, i, j):
    return i>=0 and j >=0 and i < len(graph) and j < len(graph[0])

def blocked(graph, i, j):
    return graph[i][j] == '#'

def print_graph(graph):
    for row in graph:
        print(''.join(row))

if __name__ == '__main__':

    graph = [list(line.strip()) for line in sys.stdin]

    print_graph(graph)


    curr_i, curr_j = -1, -1
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j] == '^':
                curr_i, curr_j = i, j
                break
    print(curr_i, curr_j)
    directions = {
        '^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1)
    }
    while True:
        direction = graph[curr_i][curr_j]
        di, dj = directions[direction]
        new_i, new_j = curr_i + di, curr_j + dj
        if not within_bounds(graph, new_i, new_j):
            graph[curr_i][curr_j] = 'X'
            break
        if blocked(graph, new_i, new_j):
            graph[curr_i][curr_j] = get_next(graph[curr_i][curr_j])
            continue
        graph[curr_i][curr_j] = 'X'
        curr_i, curr_j = new_i, new_j
        graph[curr_i][curr_j] = direction

    print_graph(graph)

    total = 0
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j] == 'X':
                total = total + 1
    print(total)
