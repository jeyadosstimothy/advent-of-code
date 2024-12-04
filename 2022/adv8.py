import sys

graph = []
visible = []
left = []
right = []
top = []
bottom = []

for line in sys.stdin:
    graph.append([int(x) for x in line.strip()])
    visible.append([0 for _ in line.strip()])
    left.append([0 for _ in line.strip()])
    right.append([0 for _ in line.strip()])
    top.append([0 for _ in line.strip()])
    bottom.append([0 for _ in line.strip()])

for i in range(len(graph)):
    curr_max = -1
    for j in range(len(graph[i])):
        if(graph[i][j] > curr_max):
            visible[i][j] = 1
            curr_max = graph[i][j]
        if(j == 0):
            continue

        left[i][j] = 1
        prev_max = j-1
        while(graph[i][j] > graph[i][prev_max]):
            left[i][j] = max(left[i][j], left[i][prev_max] + j - prev_max)
            if(prev_max == 0):
                break;
            prev_max = prev_max - left[i][prev_max]

    curr_max = -1
    for j in range(len(graph[i])):
        jj = -j-1
        if(graph[i][jj] > curr_max):
            visible[i][jj] = 1
            curr_max = graph[i][jj]
        if(jj == -1):
            continue

        right[i][jj] = 1
        prev_max = jj+1
        while(graph[i][jj] > graph[i][prev_max]):
            right[i][jj] = max(right[i][jj], right[i][prev_max] + prev_max - jj)
            if(prev_max == -1):
                break;
            prev_max = prev_max + right[i][prev_max]


    curr_max = -1
    for j in range(len(graph[i])):
        if(graph[j][i] > curr_max):
            visible[j][i] = 1
            curr_max = graph[j][i]
        if(j == 0):
            continue

        top[j][i] = 1
        prev_max = j-1
        while(graph[j][i] > graph[prev_max][i]):
            top[j][i] = max(top[j][i], top[prev_max][i] + j - prev_max)
            if(prev_max == 0):
                break;
            prev_max = prev_max - top[prev_max][i]

    curr_max = -1
    for j in range(len(graph[i])):
        jj = -j-1
        if(graph[jj][i] > curr_max):
            visible[jj][i] = 1
            curr_max = graph[jj][i]
        if(jj == -1):
            continue

        bottom[jj][i] = 1
        prev_max = jj+1
        while(graph[jj][i] > graph[prev_max][i]):
            bottom[jj][i] = max(bottom[jj][i], bottom[prev_max][i] + prev_max - jj)
            if(prev_max == -1):
                break;
            prev_max = prev_max + bottom[prev_max][i]

max_score = -1
for i in range(len(graph)):
    for j in range(len(graph[i])):
        score = left[i][j] * right[i][j] * top[i][j] * bottom[i][j]
        if(score > max_score):
            max_score = score

print(max_score)

def pprint(grid):
    for i in grid:
        print(i)

print("Left:")
pprint(left)
print("Right:")
pprint(right)
print("Top:")
pprint(top)
print("Bottom:")
pprint(bottom)

