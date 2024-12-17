import sys

# With help from testcases at https://www.reddit.com/r/adventofcode/comments/1hfhgl1/2024_day_16_part_1_alternate_test_case/

directions = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

def turn(direction, offset):
    s = '^>v<'
    new = (s.find(direction) + offset) % 4
    return s[new]

def flip(direction):
    return turn(direction, 2)

def move(i, j, direction):
    di, dj = directions[direction]
    return i + di, j + dj

def within_bounds(graph, i, j):
    return i>=0 and j >=0 and i < len(graph) and j < len(graph[0])

if __name__ == '__main__':
    
    graph = [list(line.strip()) for line in sys.stdin]
    si, sj = None, None
    ei, ej = None, None
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] == 'S':
                si, sj = i, j
            if graph[i][j] == 'E':
                ei, ej = i, j

    costs = {direction: [[None for _ in row] for row in graph] for direction in directions}
    queue = [('>', si, sj, 0)]
    while len(queue) != 0:
        direction, i, j, cost = queue[0]
        queue = queue[1:]
        existing_cost = costs[direction][i][j]
        if existing_cost is not None and cost >= existing_cost:
            continue
        costs[direction][i][j] = cost
        if graph[i][j] == 'E':
            continue
        ni, nj = move(i, j, direction)
        if graph[ni][nj] != '#':
            queue.append((direction, ni, nj, cost + 1))
        turns = [-1, 1, 2]
        for offset in turns:
            next_direction = turn(direction, offset)
            queue.append((next_direction, i, j, cost + abs(1000 * offset)))
    min_cost = min(costs[d][ei][ej] for d in directions if costs[d][ei][ej] is not None)
    print('Part 1:', min_cost)

    queue = [(d, ei, ej) for d in directions if costs[d][ei][ej] == min_cost]
    tiles = set()
    tiles.add((ei, ej))
    while len(queue) != 0:
        d, i, j = queue[0]
        queue = queue[1:]
        # print(d, i, j)
        cost = costs[d][i][j]
        mi, mj = move(i, j, flip(d))
        if within_bounds(graph, mi, mj) and costs[d][mi][mj] is not None and costs[d][mi][mj] + 1 == costs[d][i][j] and (mi, mj) not in tiles:
            queue.append((d, mi, mj))
            tiles.add((mi, mj))
        turns = [-1, 1]
        for offset in turns:
            td = turn(d, offset)
            if costs[td][i][j] is not None and costs[td][i][j] + abs(1000 * offset) == costs[d][i][j]:
                queue.append((td, i, j))

    print('Part 2:', len(tiles))

