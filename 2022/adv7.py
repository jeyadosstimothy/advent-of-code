import sys

directory_structure = {}
curr_path = []

def update(path, value):
    curr_dir = directory_structure
    for i in range(len(path)):
        dir = path[i]
        if(i == len(path) - 1):
            curr_dir[dir] = value
            break
        if(dir not in curr_dir):
            curr_dir[dir] = {}
        curr_dir = curr_dir[dir]


for line in sys.stdin:
    parts = line.strip().split(' ')
    if(parts[0] == '$'):
        if(parts[1] == 'cd'):
            if(parts[2] == '/'):
                curr_path = []
            elif(parts[2] == '..'):
                curr_path = curr_path[:-1]
            else:
                curr_path.append(parts[2])
    else:
        if(parts[0] == 'dir'):
            update(curr_path + [parts[1]], {})
        else:
            update(curr_path + [parts[1]], int(parts[0]))


curr_min = 70000000
curr_path = []
required = 30000000 - (70000000 - 48748071)


def dfs(node):
    if(not isinstance(node, dict)):
        return node
    total = 0
    for _, value in node.items():
        total = total + dfs(value)
    if(total >= required):
        global curr_min
        if(total < curr_min):
            curr_min = total
    return total

occupied = dfs(directory_structure)
print(curr_min)
