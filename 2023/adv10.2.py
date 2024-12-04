import sys

directions_map = {
    'S': {'U', 'D', 'L', 'R'},
    '-': {'L', 'R'},
    '|': {'U', 'D'},
    'L': {'U', 'R'},
    'F': {'R', 'D'},
    '7': {'L', 'D'},
    'J': {'L', 'U'}
}

allowed_pipes = {
    'L': ('S', '-', 'F', 'L'),
    'R': ('S', '-', 'J', '7'),
    'U': ('S', '|', '7', 'F'),
    'D': ('S', '|', 'J', 'L')
}

movements_map = {
    'L': (0, -1),
    'R': (0, 1),
    'U': (-1, 0),
    'D': (1, 0)
}

def read_graph():
    graph = []
    for line in sys.stdin:
        graph.append(list(line.strip()))
    return graph

def print_graph(graph):
    for row in graph:
        print(''.join(row))
    print()

def find_expansion_neighbours(graph, i, j):
    neighbours = []
    for mi, mj in movements_map.values():
        ni, nj = i + mi, j + mj
        if ni < 0 or ni >= len(graph):
            continue
        if nj < 0 or nj >= len(graph[i]):
            continue
        if graph[ni][nj] in {' ', '.'}:
            continue
        neighbours.append((ni, nj))
    return sorted(neighbours)

def expand_graph(graph):
    expanded = [[' '] * (len(graph[0]) * 2) for i in range(len(graph) * 2)]
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            expanded[2 * i][2 * j] = graph[i][j]
    for i in range(len(expanded)):
        for j in range(len(expanded[i])):
            if expanded[i][j] != ' ':
                continue
            neighbours = find_expansion_neighbours(expanded, i, j)
            if len(neighbours) < 2:
                expanded[i][j] = '.'
                continue
            (ai, aj), (bi, bj) = neighbours
            if ai == bi:
                if expanded[ai][aj] in allowed_pipes['L'] and expanded[bi][bj] in allowed_pipes['R']:
                    expanded[i][j] = '-'
                    continue
            if aj == bj:
                if expanded[ai][aj] in allowed_pipes['U'] and expanded[bi][bj] in allowed_pipes['D']:
                    expanded[i][j] = '|'
                    continue
            expanded[i][j] = '.'
    return expanded

def find_start(graph):
    for i in range(len(graph)):
        if 'S' not in graph[i]:
            continue
        return i, graph[i].index('S')
    raise Exception('No S')

def find_neighbours(graph, visited, i, j):
    curr = graph[i][j]
    directions = directions_map[curr]
    neighbours = []
    for d in directions:
        mi, mj = movements_map[d]
        ni, nj = i + mi, j + mj
        if ni < 0 or ni >= len(graph):
            continue
        if nj < 0 or nj >= len(graph[i]):
            continue
        if visited[ni][nj] != '.':
            continue
        if graph[ni][nj] not in allowed_pipes[d]:
            continue
        neighbours.append((ni, nj))
    return neighbours
    
def get_boundary(graph):
    boundary_graph = [['.'] * len(graph[i]) for i in range(len(graph))]
    si, sj = find_start(graph)
    boundary_graph[si][sj] = 'X'
    queue = [(si, sj)]
    while len(queue) != 0:
        ci, cj = queue[0]
        queue = queue[1:]
        for ni, nj in find_neighbours(graph, boundary_graph, ci, cj):
            queue.append((ni, nj))
            boundary_graph[ni][nj] = 'X'
    return boundary_graph


def find_flood_neighbours(graph, i, j):
    neighbours = []
    for mi, mj in movements_map.values():
        ni, nj = i + mi, j + mj
        if ni < 0 or ni >= len(graph):
            continue
        if nj < 0 or nj >= len(graph[i]):
            continue
        if graph[ni][nj] != '.':
            continue
        neighbours.append((ni, nj))
    return neighbours

def flood_fill(graph, si, sj):
    graph[si][sj] = 'O'
    queue = [(si, sj)]
    while len(queue) != 0:
        ci, cj = queue[0]
        queue = queue[1:]
        for ni, nj in find_flood_neighbours(graph, ci, cj):
            queue.append((ni, nj))
            graph[ni][nj] = 'O'
    return graph
    
def mark_outside(graph):
    for i in range(len(graph)):
        for j in (0, len(graph[i]) - 1):
            if graph[i][j] == '.':
                graph = flood_fill(graph, i, j)
    for i in (0, len(graph) - 1):
        for j in range(len(graph[i])):
            if graph[i][j] == '.':
                graph = flood_fill(graph, i, j)
    return graph

def compress_graph(graph):
    compressed = [[' '] * (len(graph[0]) // 2) for i in range(len(graph) // 2)]
    for i in range(len(compressed)):
        for j in range(len(compressed[i])):
            compressed[i][j] = graph[2 * i][2 * j]
    return compressed

def find_enclosed_tiles(graph):
    total = 0
    for row in graph:
        counts = {x: row.count(x) for x in row}
        total = total + counts.get('.', 0)
    return total

graph = read_graph()
print_graph(graph)

expanded_graph = expand_graph(graph)
print_graph(expanded_graph)

boundary_graph = get_boundary(expanded_graph)
print_graph(boundary_graph)

marked_graph = mark_outside(boundary_graph)
print_graph(marked_graph)

compressed_graph = compress_graph(marked_graph)
print_graph(compressed_graph)

result = find_enclosed_tiles(compressed_graph)
print(result)