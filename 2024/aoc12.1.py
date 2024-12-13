import math
import sys


graph = [list(row.strip()) for row in sys.stdin]
visited = [[False for _ in row] for row in graph]


def within_bounds(i, j, graph ):
    return i >= 0 and j >= 0 and i < len(graph) and j < len(graph[0])

directions = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}
def traverse_region(i, j, graph, visited):
    visited[i][j] = True
    total_area, total_perimeter = 0, 0
    this_area, this_perimeter = 1, 0
    for d in directions:
        di, dj = directions[d]
        ni, nj = i + di, j + dj
        if within_bounds(ni, nj, graph) and graph[i][j] == graph[ni][nj]:
            if not visited[ni][nj]:
                area, perimeter = traverse_region(ni, nj, graph, visited)
                total_area, total_perimeter = total_area + area, total_perimeter + perimeter
        else:
            this_perimeter = this_perimeter + 1
    total_area = total_area + this_area
    total_perimeter = total_perimeter + this_perimeter
    return total_area, total_perimeter

price = 0
for i in range(len(graph)):
    for j in range(len(graph[i])):
        if not visited[i][j]:
            area, perimeter = traverse_region(i, j, graph, visited)
            price = price + area * perimeter

print(price)
    
