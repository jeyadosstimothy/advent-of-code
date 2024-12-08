from pprint import pprint
import sys

def read_graph():
    graph = [row.strip() for row in sys.stdin]
    antennas = dict()
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            c = graph[i][j] 
            if c != '.':
                antennas[c] = antennas.get(c, []) + [(i, j)]
    bounds = (len(graph), len(graph[0]))
    return antennas, bounds

def within_bounds(i, j, bounds):
    return i>=0 and j >=0 and i < bounds[0] and j < bounds[1]

def get_anti_nodes(first, second, bounds):
    i_diff, j_diff = first[0] - second[0], first[1] - second[1]
    antinodes = [first, second]
    prev = first[0] + i_diff, first[1] + j_diff
    while within_bounds(*prev, bounds):
        antinodes.append(prev)
        prev = prev[0] + i_diff, prev[1] + j_diff
    next = second[0] - i_diff, second[1] - j_diff
    while within_bounds(*next, bounds):
        antinodes.append(next)
        next = next[0] - i_diff, next[1] - j_diff
    return antinodes

def print_graph(antennas, antinodes, bounds):
    graph = []
    for i in range(bounds[0]):
        row = []
        for j in range(bounds[1]):
            if (i, j) in antinodes:
                row.append('#')
            else:
                row.append('.')
        graph.append(row)
    
    for freq in antennas:
        for i, j in antennas[freq]:
            if graph[i][j] == '.':
                graph[i][j] = freq
    for i in range(len(graph)):
        print(f'{i:03d}', ''.join(graph[i]))
    print()


antennas, bounds = read_graph()
# pprint(antennas)

antinodes = set()
for freq in antennas:
    locations = antennas[freq]
    for i in range(len(locations)):
        for j in range(i+1, len(locations)):
            antinodes.update(get_anti_nodes(locations[i], locations[j], bounds))
# print_graph(antennas, antinodes, bounds)
print(len(antinodes))