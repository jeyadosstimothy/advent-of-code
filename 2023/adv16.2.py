import sys

def read_grid():
    grid = []
    for line in sys.stdin:
        grid.append(list(line.strip()))
    return grid

def print_grid(grid):
    for line in grid:
        print(line)
    print()

def move(i, j, d):
    directions = {
        '^': (-1, 0),
        '<': (0, -1),
        'v': (1, 0),
        '>': (0, 1)
    }
    di, dj = directions[d]
    return i + di, j + dj

def reflect(mirror, d):
    directions = {
        '\\': {
            '>': 'v',
            'v': '>',
            '<': '^',
            '^': '<'
        },
        '/': {
            '>': '^',
            '^': '>',
            '<': 'v',
            'v': '<'
        }
    }
    return directions[mirror][d]

def energize(grid, si, sj, sd):
    visited = {}
    queue = [(si, sj, sd)]
    while len(queue) != 0:
        i, j, d = queue[0]
        queue = queue[1:]
        if (i, j, d) in visited:
            continue
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
            continue
        visited[(i, j, d)] = True
        if grid[i][j] == '.':
            queue.append((*move(i, j, d), d))
        if grid[i][j] == '|':
            if d == '<' or d == '>':
                queue.append((*move(i, j, '^'), '^'))
                queue.append((*move(i, j, 'v'), 'v'))
            else:
                queue.append((*move(i, j, d), d))
        if grid[i][j] == '-':
            if d == '^' or d == 'v':
                queue.append((*move(i, j, '<'), '<'))
                queue.append((*move(i, j, '>'), '>'))
            else:
                queue.append((*move(i, j, d), d))
        if grid[i][j] == '\\' or grid[i][j] == '/':
            nd = reflect(grid[i][j], d)
            queue.append((*move(i, j, nd), nd))
    return visited

def find_max(grid):
    max_energized = 0
    for j in range(len(grid[0])):
        visited = energize(grid, 0, j, 'v')
        energized = set((i, j) for (i, j, d) in visited)
        max_energized = max(max_energized, len(energized))
    
    for j in range(len(grid[0])):
        visited = energize(grid, len(grid) - 1, j, '^')
        energized = set((i, j) for (i, j, d) in visited)
        max_energized = max(max_energized, len(energized))
    

    for i in range(len(grid)):
        visited = energize(grid, i, 0, '>')
        energized = set((i, j) for (i, j, d) in visited)
        max_energized = max(max_energized, len(energized))
    
    for i in range(len(grid)):
        visited = energize(grid, i, len(grid[0]) - 1, '<')
        energized = set((i, j) for (i, j, d) in visited)
        max_energized = max(max_energized, len(energized))

    return max_energized

grid = read_grid()
print(find_max(grid))