import sys

first, second = [], dict()
for line in sys.stdin:
    a, b = [int(x) for x in line.strip().split(' ')]
    first.append(a)
    second[b] = second.get(b, 0) + 1

answer = 0
for x in first:
    answer = answer + x * second.get(x,0)
print(answer)
