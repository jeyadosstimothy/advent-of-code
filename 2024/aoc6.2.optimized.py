import bisect
from pprint import pprint
import sys

class Path:
    def __init__(self, path=list()):
        self.path_list = list(path)
        self.path_set = set(path)

    def add(self, i, j, direction):
        self.path_list.append((i, j, direction))
        self.path_set.add((i, j, direction))

    def contains(self, i, j, direction):
        return (i, j, direction) in self.path_set

class Graph:
    def __init__(self, bounds, obstacles_coords):
        self.bounds = bounds
        self.construct_obstacles(obstacles_coords)
        # self.print()

    def construct_obstacles(self, obstacles_coords):
        self.obstacles = {
            'i': dict(),
            'j': dict(),
            'both': set()
        }
        for i, j in obstacles_coords:
            self.add_obstacle(i, j)
        # pprint(self.obstacles)

    def add_obstacle(self, i, j):
        self.obstacles['i'][i] = self.obstacles['i'].get(i, list())
        bisect.insort(self.obstacles['i'][i], j)
        self.obstacles['j'][j] = self.obstacles['j'].get(j, list())
        bisect.insort(self.obstacles['j'][j], i)
        self.obstacles['both'].add((i, j))

    def remove_obstacle(self, i, j):
        self.obstacles['i'][i].remove(j)
        self.obstacles['j'][j].remove(i)
        self.obstacles['both'].remove((i, j))

    def print(self, path=list()):
        graph = list()
        for i in range(self.bounds[0]):
            row = list()
            for j in range(self.bounds[1]):
                if self.blocked(i, j):
                    row.append('#')
                else:
                    row.append('.')
            graph.append(row)
        for i, j, d in path:
            if self.within_bounds(i, j):
                graph[i][j] = d
        for i in range(len(graph)):
            print(f'{i:03d}', ''.join(graph[i]))
        print()

    def within_bounds(self, i, j):
        return i>=0 and j >=0 and i < self.bounds[0] and j < self.bounds[1]

    def blocked(self, i, j):
        return (i, j) in self.obstacles['both']

    def get_next_before(self, axis, k, v):
        obstacles = self.obstacles[axis].get(k, list())
        if len(obstacles) == 0:
            return -1
        idx = bisect.bisect(obstacles, v)
        if idx == 0:
            return -1
        return obstacles[idx - 1] + 1

    def get_next_after(self, axis, k, v):
        obstacles = self.obstacles[axis].get(k, list())
        bound = 0 if axis == 'i' else 1
        if len(obstacles) == 0:
            return self.bounds[bound]
        idx = bisect.bisect(obstacles, v)
        if idx == len(obstacles):
            return self.bounds[bound]
        return obstacles[idx] - 1

    def get_next(self, i, j, direction):
        if direction == '^':
            return self.get_next_before('j', j, i), j, turn(direction)
        elif direction == 'v':
            return self.get_next_after('j', j, i), j, turn(direction)
        elif direction == '<':
            return i, self.get_next_before('i', i, j), turn(direction)
        elif direction == '>':
            return i, self.get_next_after('i', i, j), turn(direction)
        else:
            raise Exception('Invalid direction')

def turn(direction):
    clockwise = '^>v<'
    return clockwise[(clockwise.find(direction) + 1)%4]

def traverse(start_i, start_j, graph):
    curr_i, curr_j = start_i, start_j
    direction = '^'
    path = Path()
    iter = 0
    while True:
        iter = iter + 1
        path.add(curr_i, curr_j, direction)
        next_i, next_j, next_direction = graph.get_next(curr_i, curr_j, direction)
        if not graph.within_bounds(next_i, next_j):
            path.add(next_i, next_j, next_direction)
            break
        if path.contains(next_i, next_j, next_direction):
            path.add(next_i, next_j, next_direction)
            # print('loop found', next_i, next_j, next_direction)
            # print_graph(graph, path)
            return 'loop found', path
        curr_i, curr_j, direction = next_i, next_j, next_direction
    return 'loop not found', path

def read_graph():
    graph = [list(line.strip()) for line in sys.stdin]
    start_i, start_j = -1, -1
    obstacles = set()
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j] == '^':
                start_i, start_j = i, j
            if graph[i][j] == '#':
                obstacles.add((i, j))
    return start_i, start_j, Graph((len(graph), len(graph[0])), obstacles),

def expand_path(path):
    expanded_path = [path[0]]
    curr_i, curr_j, curr_direction = path[0]
    path = path[1:]
    while len(path) != 0:
        next_i, next_j, next_direction = path[0]
        if curr_i == next_i:
            while curr_j != next_j:
                curr_j = curr_j + (1 if curr_direction == '>' else -1)
                expanded_path.append((curr_i, curr_j, curr_direction))
        else:
            while curr_i != next_i:
                curr_i = curr_i + (1 if curr_direction == 'v' else -1)
                expanded_path.append((curr_i, curr_j, curr_direction))
        curr_direction = next_direction
        expanded_path.append((curr_i, curr_j, curr_direction))
        path = path[1:]
    return expanded_path

if __name__ == '__main__':
    start_i, start_j, graph = read_graph()
    # print('Start:', start_i, start_j)
    _, path = traverse(start_i, start_j, graph)
    expanded_path = expand_path(path.path_list)
    possible_obstacle_placements = set((i, j) for i, j, d in expanded_path if (i, j) != (start_i, start_j))
    total = 0
    for obstacle in possible_obstacle_placements:
        graph.add_obstacle(*obstacle)
        loop_status, loop_path = traverse(start_i, start_j, graph)
        if loop_status == 'loop found':
            total = total + 1
            # print('Obstacle:', obstacle)
            # graph.print(expand_path(loop_path.path_list))
        graph.remove_obstacle(*obstacle)
    print(total)
