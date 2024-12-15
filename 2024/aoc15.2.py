import sys

directions = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

def get_next(i, j, direction):
    di, dj = directions[direction]
    return i + di, j + dj

def move_robot(graph, i, j, ni, nj):
    graph[i][j] = '.'
    graph[ni][nj] = '@'
    return ni, nj

def print_graph(graph):
    for row in graph:
        print(''.join(row))
    print()

def expand_graph(graph):
    expanded_graph = []
    for row in graph:
        expanded_row = []
        for c in row:
            if c == '@':
                expanded_row.extend(['@', '.'])
            elif c == '#':
                expanded_row.extend(['#', '#'])
            elif c == 'O':
                expanded_row.extend(['[', ']'])
            else:
                expanded_row.extend(['.', '.'])
        expanded_graph.append(expanded_row)
    return expanded_graph

def calculate(graph):
    total = 0
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] == '[':
                total = total + i * 100 + j
    return total

class Box:
    def __init__(self, i, j, graph):
        self.si, self.sj, self.ei, self.ej = None, None, None, None
        if graph[i][j] == '[':
            self.si, self.sj, self.ei, self.ej = i, j, i, j + 1
        else:
            self.si, self.sj, self.ei, self.ej = i, j - 1, i, j
        self.graph = graph
    
    def __repr__(self):
        return f'(s:{self.si, self.sj}), e:{self.ei, self.ej})'
        
    def check_next(self, direction):
        nsi, nsj = get_next(self.si, self.sj, direction)
        if self.graph[nsi][nsj] == '#':
            return None
        nei, nej = get_next(self.ei, self.ej, direction)
        if self.graph[nei][nej] == '#':
            return None
        new = graph[nsi][nsj] + graph[nei][nej]
        if new == '..':
            return []
        if new == '].':
            return [Box(nsi, nsj, self.graph)]
        if new == '.[':
            return [Box(nei, nej, self.graph)]
        if new == '[]':
            return [Box(nsi, nsj, self.graph)]
        if new == '][':
            return [Box(nsi, nsj, self.graph), Box(nei, nej, self.graph)]
    
    def move(self, direction):
        (nsi, nsj), (nei, nej) = get_next(self.si, self.sj, direction), get_next(self.ei, self.ej, direction)
        self.graph[nsi][nsj] = '['
        self.graph[nei][nej] = ']'
        self.graph[self.si][self.sj] = '.'
        self.graph[self.ei][self.ej] = '.'

if __name__ == '__main__':
    
    graph = []
    for line in sys.stdin:
        if len(line.strip()) == 0:
            break
        graph.append(list(line.strip()))
    graph = expand_graph(graph)

    movements = []
    for line in sys.stdin:
        movements.extend(list(line.strip()))
    
    si, sj = None, None
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] == '@':
                si, sj = i, j
    
    i, j = si, sj
    iter = 0
    for direction in movements:
        print_graph(graph)
        ni, nj = get_next(i, j, direction)
        print(iter, direction, (i, j), graph[ni][nj])
        iter = iter + 1
        if graph[ni][nj] == '#':
            continue
        if graph[ni][nj] not in '[]':
            i, j = move_robot(graph, i, j, ni, nj)
            continue
        if direction in '<>':
            ii, jj = ni, nj
            while graph[ii][jj] in '[]':
                ii, jj = get_next(ii, jj, direction)
            if graph[ii][jj] == '#':
                continue
            ii, jj = ni, nj
            prev = graph[ii][jj]
            while True:
                print(ii, jj, ni, nj, graph[ii][jj], prev)
                ii, jj = get_next(ii, jj, direction)
                temp = graph[ii][jj]
                graph[ii][jj] = prev
                prev = temp
                if temp == '.':
                    break
            i, j = move_robot(graph, i, j, ni, nj)
            continue
        if direction in '^v':
            queue = [[Box(ni, nj, graph)]]
            boxes_to_move = list()
            reached_wall = False
            while not reached_wall and len(queue) != 0:
                print(queue)
                boxes_in_curr_level = queue[0]
                boxes_to_move.extend(boxes_in_curr_level)
                queue = queue[1:]
                boxes_in_next_level = []
                for box in boxes_in_curr_level:
                    next_boxes = box.check_next(direction)
                    if next_boxes is None:
                        reached_wall = True
                        break
                    boxes_in_next_level.extend(next_boxes)
                if len(boxes_in_next_level) != 0:
                    queue.append(boxes_in_next_level)
                
            if reached_wall:
                continue
            for box in reversed(boxes_to_move):
                box.move(direction)
            i, j = move_robot(graph, i, j, ni, nj)

    
    print_graph(graph)
    print(calculate(graph))
