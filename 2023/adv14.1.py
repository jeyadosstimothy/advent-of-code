import sys

def read_grid():
    grid = []
    for line in sys.stdin:
        grid.append(list(line.strip()))
    return grid

def print_grid(grid):
    for line in grid:
        print(''.join(line))
    print()

def tilt_north(grid):
    for col in range(len(grid[0])):
        curr, empty = 0, 0
        while True:
            while empty < len(grid) and grid[empty][col] != '.':
                empty = empty + 1
            curr = empty
            while curr < len(grid) and grid[curr][col] == '.':
                curr = curr + 1
            while curr < len(grid) and grid[curr][col] == 'O':
                grid[empty][col] = 'O'
                grid[curr][col] = '.'
                empty = empty + 1
                curr = curr + 1
            if curr < len(grid) and grid[curr][col] == '#':
                empty = curr
            if curr >= len(grid):
                break

def calculate_load(grid):
    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'O':
                total = total + len(grid) - i
    return total

grid = read_grid()
print_grid(grid)
tilt_north(grid)
print_grid(grid)
print(calculate_load(grid))