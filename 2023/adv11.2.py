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

expansion_rate = 1000000 - 1
galaxies = []
di = 0
for i in range(len(grid)):
    if i not in i_galaxies:
        di = di + expansion_rate
    dj = 0
    for j in range(len(grid[i])):
        if j not in j_galaxies:
            dj = dj + expansion_rate
        if grid[i][j] == '#':
            galaxies.append((i + di, j + dj))            

total = 0
for i in range(len(galaxies)):
    for j in range(i+1, len(galaxies)):
        (i1, j1), (i2, j2) = galaxies[i], galaxies[j]
        dist = abs(i1 - i2) + abs(j1 - j2)
        total = total + dist
print(total)