from pprint import pprint
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

def within_bounds(i, j, graph):
    return i >= 0 and j >= 0 and i < len(graph) and j < len(graph[0])

def manhattan(si, sj, ei, ej):
    return abs(ei - si) + abs(ej - sj)

def find_shortest_path(graph, ei, ej):
    queue = [(ei, ej)]
    distances = [[None for _ in row] for row in graph]
    distances[ei][ej] = 0
    path = []

    while len(queue) != 0:
        i, j = queue[0]
        queue = queue[1:]
        path.append((i, j))

        if graph[i][j] == 'S':
            break

        for d in directions:
            ni, nj = get_next(i, j, d)
            if graph[ni][nj] == '#' or distances[ni][nj] is not None:
                continue
            queue.append((ni, nj))
            distances[ni][nj] = distances[i][j] + 1
    return list(reversed(path)), distances

def get_cheat_endpoints(graph, cheat_validity, si, sj):
    queue = [(si, sj)]
    visited = set()
    endpoints = list()
    while len(queue) != 0:
        i, j = queue[0]
        queue = queue[1:]

        if (i, j) != (si, sj) and graph[i][j] != '#':
            endpoints.append((i, j))
        
        for d in directions:
            ni, nj = get_next(i, j, d)
            if not within_bounds(ni, nj, graph) or (ni, nj) in visited or manhattan(si, sj, ni, nj) > cheat_validity:
                continue
            queue.append((ni, nj))
            visited.add((ni, nj))
    return endpoints

if __name__ == '__main__':
    cheat_validity, steps_to_save = map(int, sys.stdin.readline().strip().split(', '))
    graph = [list(line.strip()) for line in sys.stdin]
    si, sj = None, None
    ei, ej = None, None
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] == 'S':
                si, sj = i, j
            if graph[i][j] == 'E':
                ei, ej = i, j

    path, distances = find_shortest_path(graph, ei, ej)
    print(distances[si][sj])
    print(path)

    visited = set()
    cheats = dict()
    for step in range(len(path) - 1):
        curr = path[step]
        # print("curr", curr, step)
        visited.add(curr)
        cheat_endpoints = get_cheat_endpoints(graph, cheat_validity, *curr)
        # print(cheat_endpoints)
        for cheat_endpoint in cheat_endpoints:
            ci, cj = cheat_endpoint
            distance_with_cheat = step + manhattan(*curr, *cheat_endpoint) + distances[ci][cj]
            if distance_with_cheat < distances[si][sj]:
                steps_saved = distances[si][sj] - distance_with_cheat
                cheat_set = cheats.get(steps_saved, set())
                cheat_set.add((curr, cheat_endpoint))
                cheats[steps_saved] = cheat_set
    pprint(cheats)
    steps_saved_to_num_cheats = [(len(cheats[steps_saved]), steps_saved) for steps_saved in cheats if steps_saved >= steps_to_save]
    pprint(list(sorted(steps_saved_to_num_cheats, key=lambda x: x[1])))
    print(sum(num_cheats for num_cheats, _  in steps_saved_to_num_cheats))
