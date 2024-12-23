from pprint import pprint
import re
import sys

number_key_pad = [
    '789',
    '456',
    '123',
    '#0A'
]
number_keys = 'A0123456789'
direction_key_pad = [
    '#^A',
    '<v>'
]
direction_keys = 'A^>v<'

directions = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

def get_next(i, j, direction):
    di, dj = directions[direction]
    return i + di, j + dj

def within_bounds(i, j, graph):
    return i >= 0 and j >= 0 and i < len(graph) and j < len(graph[0])

def moves_for_graph(graph, start):
    si, sj = None, None
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] == start:
                si, sj = i, j
                break
    
    paths = [[[] for j in range(len(graph[0]))] for i in range(len(graph))]
    queue = [(si, sj, '')]
    while len(queue) != 0:
        i, j, moves = queue[0]
        queue = queue[1:]
        final_moves = moves + 'A'
        if len(paths[i][j]) == 0:
            paths[i][j] = [final_moves]
        elif len(paths[i][j]) != 0:
            if len(final_moves) < len(paths[i][j][0]):
                paths[i][j] = [final_moves]
            elif len(final_moves) == len(paths[i][j][0]):
                paths[i][j].append(final_moves)
            else:
                continue

        for d in directions:
            ni, nj = get_next(i, j, d)
            if not within_bounds(ni, nj, graph) or graph[ni][nj] == '#':
                continue
            queue.append((ni, nj, moves + d))
    path_dict = dict()
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] == '#':
                continue
            path_dict[(graph[si][sj], graph[i][j])] = paths[i][j]
    return path_dict

numeric_paths_dict = dict()
for s in number_keys:
    numeric_paths_dict.update(moves_for_graph(number_key_pad, s))

direction_paths_dict = dict()
for s in direction_keys:
    direction_paths_dict.update(moves_for_graph(direction_key_pad, s))

def find_shortest_sequence_for_keys(paths_dict, from_key, to_key, depth, num_directional_robots, memoized):
    print(from_key, to_key, depth, end=' ')
    if (from_key, to_key, depth) in memoized:
        print('memoized')
        return memoized[(from_key, to_key, depth)]
    print()

    paths = paths_dict[(from_key, to_key)]
    min_length = None
    for path in paths:
        prev = 'A'
        path_length = 0
        if depth < num_directional_robots:
            for curr in path:
                path_length = path_length + find_shortest_sequence_for_keys(direction_paths_dict, prev, curr, depth + 1, num_directional_robots, memoized)
                prev = curr
        else:
            path_length = len(path)
        if min_length is None or path_length < min_length:
            min_length = path_length
    memoized[(from_key, to_key, depth)] = min_length
    return min_length

def find_shortest_sequence(sequence, num_directional_robots, memoized):
    prev = 'A'
    path_length = 0
    for curr in sequence:
        path_length = path_length + find_shortest_sequence_for_keys(numeric_paths_dict, prev, curr, 0, num_directional_robots, memoized)
        prev = curr
    return path_length

if __name__ == '__main__':

    sequences = [line.strip() for line in sys.stdin]

    complexity = 0
    memoized = dict()
    for sequence in sequences:
        print("Sequence:", sequence)
        final_sequence_length = find_shortest_sequence(sequence, 25, memoized)
        print("Final:", final_sequence_length)
        complexity = complexity + final_sequence_length * int(re.findall(r'\d+', sequence)[0])
    print(complexity)