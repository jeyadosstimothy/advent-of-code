import sys

def turn(direction):
    clockwise = '^>v<'
    return clockwise[(clockwise.find(direction) + 1)%4]

def get_next(i, j, direction):
    directions = {
        '^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1)
    }
    di, dj = directions[direction]
    return i + di, j + dj

def within_bounds(graph, i, j):
    return i>=0 and j >=0 and i < len(graph) and j < len(graph[0])

def blocked(graph, i, j):
    return graph[i][j] == '#' or graph[i][j] == 'O'

def print_graph(graph, path):
    print(path.path_list)
    copy_graph = [list(row) for row in graph]
    for i, j, direction in path.path_list:
        copy_graph[i][j] = direction
    for i in range(len(copy_graph)):
        print(f'{i:03d}', ''.join(copy_graph[i]))
    print()

class Path:
    def __init__(self, path=list()):
        self.path_list = list(path)
        self.path_set = set(path)

    def add(self, i, j, direction):
        self.path_list.append((i, j, direction))
        self.path_set.add((i, j, direction))

    def contains(self, i, j, direction):
        return (i, j, direction) in self.path_set

def traverse(graph, start_i, start_j, place_obstacles=True):
    curr_i, curr_j = start_i, start_j
    obstacles_placed = set()
    direction = '^'
    path=Path()
    iter = 0
    while True:
        iter = iter + 1
        path.add(curr_i, curr_j, direction)
        next_i, next_j = get_next(curr_i, curr_j, direction)
        if not within_bounds(graph, next_i, next_j):
            break
        if blocked(graph, next_i, next_j):
            direction = turn(direction)
            continue
        if place_obstacles:
            # print(iter)
            graph[next_i][next_j] = 'O'
            loop_status, _ = traverse(graph, start_i, start_j, False)
            graph[next_i][next_j] = '.'
            if loop_status == 'loop found':
                obstacles_placed.add((next_i, next_j))
        if path.contains(next_i, next_j, direction):
            # print('Found', next_i, next_j, direction)
            # print_graph(graph, path)
            return 'loop found', obstacles_placed
        curr_i, curr_j = next_i, next_j
    return 'loop not found', obstacles_placed

def read_graph():
    graph = [list(line.strip()) for line in sys.stdin]
    start_i, start_j = -1, -1
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j] == '^':
                start_i, start_j = i, j
                break
    return start_i, start_j, graph

if __name__ == '__main__':
    start_i, start_j, graph = read_graph()
    _, obstacles = traverse(graph, start_i, start_j)
    # print(obstacles)
    print(len(obstacles))
