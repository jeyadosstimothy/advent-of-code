import sys


rope = [(0, 0)] * 10

visited = {rope[-1]}

move_dict = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0)
}

def limit(x):
    if(x % 2 == 0):
        return x / 2
    return x


for line in sys.stdin:
    dir, steps = line.strip().split(' ')
    steps = int(steps)
    move = move_dict[dir]
    
    print(dir, steps)
    while(steps != 0):
        rope[0] = (rope[0][0] + move[0], rope[0][1] + move[1])
        for i in range(len(rope) - 1):
            head = rope[i]
            tail = rope[i+1]

            diff = (head[0] - tail[0], head[1] - tail[1])

            new_tail = tail
            if(abs(diff[0]) > 1 or abs(diff[1]) > 1):
                new_tail = (tail[0] + limit(diff[0]), tail[1] + limit(diff[1]))

            rope[i+1] = new_tail
            if(new_tail == tail):
                break
        
        print(rope)
        visited.add(rope[-1])
        steps = steps - 1
    print()

print(len(visited))