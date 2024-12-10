from pprint import pprint
import sys

def within_bounds(i, j, graph):
    return i>=0 and j >=0 and i < len(graph) and j < len(graph[0])

graph = [[int(x) if x != '.' else -1 for x in row.strip()] for row in sys.stdin]
memoized = [[None for _ in row] for row in graph]

directions = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

def dfs(i, j, graph, memoized):
    if not within_bounds(i, j, graph):
        return 0
    if memoized[i][j] is not None:
        return memoized[i][j]
    if graph[i][j] == 9:
        memoized[i][j] = 1
        return 1
    total = 0
    for d in directions:
        di, dj = directions[d]
        new_i, new_j = i + di, j + dj
        if within_bounds(new_i, new_j, graph) and graph[i][j] + 1 == graph[new_i][new_j]:
            total = total + dfs(new_i, new_j, graph, memoized)
    memoized[i][j] = total
    return total
     
starts = []
for i in range(len(graph)):
    for j in range(len(graph[0])):
        if graph[i][j] == 0:
            starts.append((i, j))

total = 0
for start in starts:
    total = total + dfs(*start, graph, memoized)
print(total)
