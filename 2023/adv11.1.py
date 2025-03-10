import sys

grid = []
for line in sys.stdin:
    grid.append(line.strip())

i_galaxies = set()
j_galaxies = set()
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == '#':
            i_galaxies.add(i)
            j_galaxies.add(j)

expanded = []
for i in range(len(grid)):
    row = ''
    for j in range(len(grid[i])):
        if j not in j_galaxies:
            row = row + '.'
        row = row + grid[i][j]
    expanded.append(row)
    if i not in i_galaxies:
        expanded.append(row)

galaxies = []
for i in range(len(expanded)):
    for j in range(len(expanded[i])):
        if expanded[i][j] == '#':
            galaxies.append((i, j))

total = 0
for i in range(len(galaxies)):
    for j in range(i+1, len(galaxies)):
        (i1, j1), (i2, j2) = galaxies[i], galaxies[j]
        dist = abs(i1 - i2) + abs(j1 - j2)
        total = total + dist
print(total)