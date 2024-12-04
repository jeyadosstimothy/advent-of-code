import sys


def getS(grid):
    for i in range(len(grid)):
        j = grid[i].find("S")
        if j != -1:
            return (i, j)
    raise Exception("No start found")


def findPossibleNeighbours(grid, distances, i, j):
    neighbours = []
    movements = [
        (0, -1, {"-", "L", "F"}),
        (-1, 0, {"|", "F", "7"}),
        (0, 1, {"-", "7", "J"}),
        (1, 0, {"|", "J", "L"}),
    ]
    for di, dj, allowed_pipes in movements:
        if i + di < 0 or i + di >= len(grid):
            continue
        if j + dj < 0 or j + dj >= len(grid[i]):
            continue
        if distances[i + di][j + dj] != -1:
            continue
        if grid[i + di][j + dj] not in allowed_pipes:
            continue
        neighbours.append((i + di, j + dj))
    return neighbours


def findFarthest(grid):
    distances = [[-1] * len(grid[0]) for i in range(len(grid))]
    si, sj = getS(grid)
    distances[si][sj] = 0

    queue = [(si, sj)]
    while len(queue) != 0:
        ci, cj = queue[0]
        queue = queue[1:]
        neighbours = findPossibleNeighbours(grid, distances, ci, cj)
        for ni, nj in neighbours:
            distances[ni][nj] = distances[ci][cj] + 1
        queue.extend(neighbours)

    return max([max(row) for row in distances])


grid = []
for line in sys.stdin:
    grid.append(line.strip())

print(findFarthest(grid))
