import sys

graph = []
visited = []
starts = []
end = None
i = 0
for line in sys.stdin:
    row = list(line.strip())
    for j in range(len(row)):
        if(row[j] == 'S' or row[j] == 'a'):
            starts.append((i, j))
        if(row[j] == 'E'):
            end = (i, j)
    graph.append(row)
    visited.append([-1] * len(row))
    i = i + 1

queue = [*starts]
for i, j in queue:
    visited[i][j] = 0


def ord2(c):
    if c == 'S':
        return ord('a')
    if c == 'E':
        return ord('z')
    return ord(c)

def is_valid(from_, to):
    return ord2(from_) >= ord2(to) or ord2(from_) + 1 == ord2(to) 

while(len(queue) != 0):
    print(queue)

    i, j = queue[0]
    queue = queue[1:]

    if(i + 1 < len(graph) and is_valid(graph[i][j], graph[i+1][j]) and visited[i+1][j] == -1):
        queue.append((i+1, j))
        visited[i+1][j] = visited[i][j] + 1
    if(j + 1 < len(graph[i]) and is_valid(graph[i][j], graph[i][j+1]) and visited[i][j+1] == -1):
        queue.append((i, j+1))
        visited[i][j+1] = visited[i][j] + 1
    if(i - 1 >= 0 and is_valid(graph[i][j], graph[i-1][j]) and visited[i-1][j] == -1):
        queue.append((i-1, j))
        visited[i-1][j] = visited[i][j] + 1
    if(j - 1 >= 0 and is_valid(graph[i][j], graph[i][j-1]) and visited[i][j-1] == -1):
        queue.append((i, j-1))
        visited[i][j-1] = visited[i][j] + 1

print(visited[end[0]][end[1]])