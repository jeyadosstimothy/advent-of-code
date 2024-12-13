import math
import sys


def within_bounds(i, j, graph ):
    return i >= 0 and j >= 0 and i < len(graph) and j < len(graph[0])

directions = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}
orientation = {
    '^': 'h',
    '>': 'v',
    'v': 'h',
    '<': 'v'
}
def get_border_coordinate(d, i, j, ni, nj):
    if d == '^' or d == '<':
        return (orientation[d], i, j)
    return (orientation[d], ni, nj)
    
def traverse_region(start_i, start_j, graph, visited):
    area, perimeter, borders = 0, 0, set()

    queue = [(start_i, start_j)]
    visited[start_i][start_j] = True
    while len(queue) != 0:
        i, j = queue[0]
        queue = queue[1:]
        # print(i,j, graph[i][j])
        area = area + 1
        for d in directions:
            di, dj = directions[d]
            ni, nj = i + di, j + dj
            if within_bounds(ni, nj, graph) and graph[i][j] == graph[ni][nj]:
                if not visited[ni][nj]:
                    queue.append((ni, nj))
                    visited[ni][nj] = True
                else:
                    pass
            else:
                perimeter = perimeter + 1
                borders.add(get_border_coordinate(d, i, j, ni, nj))
    return area, perimeter, borders

def print_graph(graph):
    for row in graph:
        print(''.join(row))
    print()

def num_sides(borders):
    #print(borders)
    h_borders = sorted([(border[1], border[2]) for border in borders if border[0] == 'h'])
    v_borders = sorted([(border[2], border[1]) for border in borders if border[0] == 'v'])
    h_sides = 1
    for i in range(1, len(h_borders)):
        (x1, y1), (x2, y2) = h_borders[i-1], h_borders[i]
        if (x1 == x2 and y1 + 1 == y2):
            continue
        h_sides = h_sides + 1
    v_sides = 1
    for i in range(1, len(v_borders)):
        (y1, x1), (y2, x2) = v_borders[i-1], v_borders[i]
        if (y1 == y2 and x1 + 1 == x2):
            continue
        v_sides = v_sides + 1
    #print(h_sides, h_borders)
    #print(v_sides, v_borders)
    return h_sides + v_sides

def expand_graph(graph):
    expanded_graph = []
    for i in range(len(graph) * 2):
        row = []
        for j in range(len(graph[0]) * 2):
            ii = i // 2
            jj = j // 2
            if i % 2 == 0 and j % 2 == 0:
                row.append(graph[ii][jj])
            elif i % 2 == 0:
                if within_bounds(ii, jj + 1, graph) and graph[ii][jj] == graph[ii][jj + 1]:
                    row.append(graph[ii][jj])
                else:
                    row.append('.')
            else:
                row.append('.')
        expanded_graph.append(row)
    for i in range(len(graph) * 2):
        for j in range(len(graph[0]) * 2):
            if i % 2 == 1 and within_bounds(i + 1, j, expanded_graph) and expanded_graph[i - 1][j] == expanded_graph[i + 1][j]:
                expanded_graph[i][j] = expanded_graph[i-1][j]
    return expanded_graph


graph = [list(row.strip()) for row in sys.stdin]
visited = [[False for _ in row] for row in graph]

# print_graph(graph)
expanded_graph = expand_graph(graph)
print_graph(expanded_graph)
expanded_visited = [[False for _ in row] for row in expanded_graph]

price = 0
for i in range(len(graph)):
    for j in range(len(graph[i])):
        if not visited[i][j]:
            # print('traverse normal')
            area, perimeter, _ = traverse_region(i, j, graph, visited)
            # print('traverse expanded')
            _, _, borders = traverse_region(2*i, 2*j, expanded_graph, expanded_visited)
            sides = num_sides(borders)
            price = price + area * sides
            # print(graph[i][j], area, sides, price)
print(price)
    
