import sys

directions = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

def move(pos, direction):
    i, j = pos
    di, dj = directions[direction]
    return i + di, j + dj

def print_graph(robot, walls, boxes, bounds):
    for i in range(bounds[0]):
        row = ''
        for j in range(bounds[1]):
            if (i, j) == robot:
                row = row + '@'
            elif (i, j) in walls:
                row = row + '#'
            elif (i, j) in boxes:
                row = row + 'O'
            else:
                row = row + '.'
        print(row)
    print()

def calculate(boxes, bounds):
    total = 0
    for i in range(bounds[0]):
        for j in range(bounds[1]):
            if (i, j) in boxes:
                total = total + i * 100 + j
    return total

if __name__ == '__main__':
    
    graph = []
    for line in sys.stdin:
        if len(line.strip()) == 0:
            break
        graph.append(list(line.strip()))

    movements = []
    for line in sys.stdin:
        movements.extend(list(line.strip()))
    
    robot = None
    walls, boxes = set(), set()
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] == '@':
                robot = (i, j)
            elif graph[i][j] == '#':
                walls.add((i, j))
            elif graph[i][j] == 'O':
                boxes.add((i, j))
            else:
                continue
    bounds = len(graph), len(graph[0])
    print_graph(robot, walls, boxes, bounds)
    
    for direction in movements:
        new = move(robot, direction)
        if new in walls:
            continue
        if new not in boxes:
            robot = new
            continue
        it = new
        while it in boxes:
            it = move(it, direction)
        if it in walls:
            continue
        boxes.add(it)
        boxes.remove(new)
        robot = new
    
    print_graph(robot, walls, boxes, bounds)
    print(calculate(boxes, bounds))

        
    
