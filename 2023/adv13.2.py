import sys

def read_grid():
    grid = []
    has_next = False
    for line in sys.stdin:
        if len(line.strip()) == 0:
            has_next = True
            break
        grid.append(line.strip())
    return grid, has_next

def print_grid(grid):
    for line in grid:
        print(line)
    print()

def convert(s):
    n = 1
    for c in s:
        n = n << 1
        if c == '#':
            n = n | 1
    return n

def count_ones(n):
    o = 0
    while n != 0:
        o = o + (n & 1)
        n = n >> 1
    return o

def find_mirror(nums):
    for i in range(1, len(nums)):
        a = nums[max(0, i + i - len(nums)):i]
        b = list(reversed(nums[i:min(i + i, len(nums))]))
        c = []
        for j in range(len(a)):
            if a[j] == b[j]:
                continue
            c.append(count_ones(a[j]^b[j]))
        if len(c) == 1 and c[0] == 1:
            return i
    return 0

def check_vertical(grid):
    nums = []
    for j in range(len(grid[0])):
        col = ''
        for i in range(len(grid)):
            col = col + grid[i][j]
        nums.append(convert(col))
    return find_mirror(nums)

def check_horizontal(grid):
    nums = []
    for i in range(len(grid)):
        row = ''
        for j in range(len(grid[i])):
            row = row + grid[i][j]
        nums.append(convert(row))
    return find_mirror(nums)
    

total = 0
has_next = True
while has_next:
    grid, has_next = read_grid()
    # print_grid(grid)
    total = total + check_vertical(grid) + 100 * check_horizontal(grid)
print(total)