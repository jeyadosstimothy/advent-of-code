import sys

class Grid:
    def __init__(self, grid):
        if len(grid) != len(grid[0]):
            raise Exception('only square grid allowed')
        self.grid = grid
        self.orientation = '^'
    
    def __len__(self):
        return len(self.grid)

    def get_ij(self, key):
        i, j = key
        if self.orientation == '^':
            return i, j
        if self.orientation == '<':
            return len(self.grid) - j - 1, i
        if self.orientation == 'v':
            return len(self.grid) - i - 1, len(self.grid) - j - 1
        if self.orientation == '>':
            return j, len(self.grid) - i - 1
        raise Exception('unexpected orientation')

    def __getitem__(self, key):
        i, j = self.get_ij(key)
        return self.grid[i][j]
    
    def __setitem__(self, key, value):
        i, j = self.get_ij(key)
        self.grid[i][j] = value
    
    def __repr__(self):
        s = ''
        for ki in range(len(self.grid)):
            row = ''
            for kj in range(len(self.grid)):
                i, j = self.get_ij((ki, kj))
                row = row + self.grid[i][j]
            s = s + row + '\n'
        return s

    def rotate(self):
        orientations = '^<v>'
        self.orientation = orientations[(orientations.find(self.orientation) + 1)%4]

def read_grid(inp):
    grid = []
    for line in inp:
        grid.append(list(line.strip()))
    return Grid(grid)

def print_grid(grid):
    for i in range(len(grid)):
        line = ''
        for j in range(len(grid)):
            line = line + grid[(i, j)]
        print(line)
    print()

def tilt_north(grid):
    for col in range(len(grid)):
        curr, empty = 0, 0
        while True:
            while empty < len(grid) and grid[(empty, col)] != '.':
                empty = empty + 1
            curr = empty
            while curr < len(grid) and grid[(curr, col)] == '.':
                curr = curr + 1
            while curr < len(grid) and grid[(curr, col)] == 'O':
                grid[(empty, col)] = 'O'
                grid[(curr, col)] = '.'
                empty = empty + 1
                curr = curr + 1
            if curr < len(grid) and grid[(curr, col)] == '#':
                empty = curr
            if curr >= len(grid):
                break

def cycle(grid):
    for _ in range(4):
        tilt_north(grid)
        grid.rotate()

def identify_loop(grid, cycles):
    seen_cache, iter_cache = {}, {}
    for i in range(1, cycles + 1):
        cycle(grid)
        curr = str(grid)
        if curr in seen_cache:
            return iter_cache, seen_cache[curr], i - seen_cache[curr]
        seen_cache[curr] = i
        iter_cache[i] = curr

def calculate_load(grid):
    total = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[(i, j)] == 'O':
                total = total + len(grid) - i
    return total

grid = read_grid(sys.stdin)
cycles = 1000000000
iter_cache, loop_start, loop_length = identify_loop(grid, cycles)
final_grid = iter_cache[((cycles - loop_start) % loop_length) + loop_start]
print(calculate_load(read_grid(final_grid.splitlines())))
