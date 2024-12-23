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

def find_shortest_sequence_for_keys(paths_dict, from_key, to_key, depth=0):
    paths = paths_dict[(from_key, to_key)]
    sequences = []
    for path in paths:
        prev = 'A'
        sequence = ''
        if depth < 2:
            for curr in path:
                sequence = sequence + find_shortest_sequence_for_keys(direction_paths_dict, prev, curr, depth + 1)
                prev = curr
        else:
            sequence = path
        sequences.append(sequence)
    return list(sorted((len(sequence), sequence) for sequence in sequences))[0][1]

def find_shortest_sequence(sequence):
    prev = 'A'
    shortest_sequence = ''
    for curr in sequence:
        shortest_sequence = shortest_sequence + find_shortest_sequence_for_keys(numeric_paths_dict, prev, curr)
        prev = curr
    return shortest_sequence

if __name__ == '__main__':

    sequences = [line.strip() for line in sys.stdin]

    complexity = 0
    for sequence in sequences:
        final_sequence = find_shortest_sequence(sequence)
        print(sequence, final_sequence)
        complexity = complexity + len(final_sequence) * int(re.findall(r'\d+', sequence)[0])
    print(complexity)