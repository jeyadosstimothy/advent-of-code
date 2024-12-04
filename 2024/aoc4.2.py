import sys

def within_bounds(graph, i, j):
    return i>=0 and j >=0 and i < len(graph) and j < len(graph[0])

def matches(graph, i, j):
    if graph[i][j] != 'A':
        raise Exception('Not A')

    directions = {
        '\\': ((-1, -1), (1, 1)),
        '/': ((1, -1), (-1, 1))
    }

    match = 1
    for direction in directions:
        pre_i, pre_j = i + directions[direction][0][0], j + directions[direction][0][1]
        if not within_bounds(graph, pre_i, pre_j):
            match = 0
            break
        post_i, post_j = i + directions[direction][1][0], j + directions[direction][1][1]
        if not within_bounds(graph, post_i, post_j):
            match = 0
            break
        mas = graph[pre_i][pre_j] + graph[i][j] + graph[post_i][post_j]
        if mas != 'MAS' and mas != 'SAM':
            match = 0
            break
    return match

def print_graph(graph):
    for row in graph:
        print(row)

if __name__ == '__main__':
    graph = [list(line.strip()) for line in sys.stdin]

    a_locations = []
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j] == 'A':
                a_locations.append((i, j))

    total = 0
    while len(a_locations) != 0:
        i, j = a_locations[0]
        total = total + matches(graph, i, j)
        a_locations = a_locations[1:]

    print(total)
