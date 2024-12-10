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
    possible_nines = set()
    if graph[i][j] == 9:
        possible_nines.add((i, j))
        memoized[i][j] = possible_nines
        return possible_nines
    for d in directions:
        di, dj = directions[d]
        new_i, new_j = i + di, j + dj
        if within_bounds(new_i, new_j, graph) and graph[i][j] + 1 == graph[new_i][new_j]:
            possible_nines.update(dfs(new_i, new_j, graph, memoized))
    memoized[i][j] = possible_nines
    return possible_nines
     
starts = []
for i in range(len(graph)):
    for j in range(len(graph[0])):
        if graph[i][j] == 0:
            starts.append((i, j))

total = 0
for start in starts:
    possible_nines = dfs(*start, graph, memoized)
    total = total + len(possible_nines)
print(total)
