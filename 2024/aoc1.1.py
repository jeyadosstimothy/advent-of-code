import sys

first, second = [], []
for line in sys.stdin:
    a, b = [int(x) for x in line.strip().split(' ')]
    first.append(a)
    second.append(b)

answer = 0
first, second = sorted(first), sorted(second)
for i in range(len(first)):
    answer = answer + abs(first[i] - second[i])
print(answer)
