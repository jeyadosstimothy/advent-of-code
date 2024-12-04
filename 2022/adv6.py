import sys

for line in sys.stdin:
    queue = []
    i = 0
    for c in line.strip():
        i = i + 1
        queue.append(c)
        my_set = set(queue)
        if(len(my_set) == 14):
            print(i)
            break
        if(len(queue) == 14):
            x = queue[0]
            queue = queue[1:]
            my_set.remove(x)