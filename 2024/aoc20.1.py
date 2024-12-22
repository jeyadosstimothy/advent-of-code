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

def cheat(graph, steps, distances, cheat_validity, si, sj, i, j, visited, short_cut, distance=0):
    # print("cheat", i, j, short_cut, distance)
    cheats = []
    if distance >= 2 and graph[i][j] != '#':
        distance_with_cheats = steps + distance + distances[i][j]
        if distance_with_cheats < distances[si][sj]:
            cheats.extend([(distance_with_cheats, short_cut)])
        return cheats

    for d in directions:
        ni, nj = get_next(i, j, d)
        if not within_bounds(ni, nj, graph) or (ni, nj) in visited:
            continue
        if distance + 1 == cheat_validity and graph[ni][nj] == '#':
            continue
        if distance == 0 and graph[ni][nj] != '#':
            continue
        visited.add((ni, nj))
        cheats.extend(cheat(graph, steps, distances, cheat_validity, si, sj, ni, nj, visited, short_cut + [(ni, nj)], distance + 1))
        visited.remove((ni, nj))
    return cheats

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
    for step in range(len(path)):
        curr = path[step]
        # print("curr", curr, step)
        visited.add(curr)
        for steps_with_cheats, short_cut in cheat(graph, step, distances, cheat_validity, si, sj, *curr, set(visited), [curr]):
            steps_saved = distances[si][sj] - steps_with_cheats
            # print("steps_saved", steps_saved, short_cut)
            if len(short_cut) == cheat_validity + 1:
                short_cut = short_cut[:-1]
            cheat_set = cheats.get(steps_saved, set())
            cheat_set.add((short_cut[0], short_cut[-1]))
            cheats[steps_saved] = cheat_set
    # pprint(cheats)
    steps_saved_to_num_cheats = [(len(cheats[steps_saved]), steps_saved) for steps_saved in cheats if steps_saved >= steps_to_save]
    pprint(list(sorted(steps_saved_to_num_cheats, key=lambda x: x[1])))
    print(sum(num_cheats for num_cheats, _  in steps_saved_to_num_cheats))
