import sys

count = 0

for line in sys.stdin:
    interval1, interval2 = [[int(x) for x in i.split('-')] for i in line.strip().split(',')]
    if(interval1[0] <= interval2[0] and interval2[0] <= interval1[1]):
        count = count + 1
    elif (interval1[0] <= interval2[1] and interval2[1] <= interval1[1]):
        count = count + 1
    elif (interval2[0] <= interval1[1] and interval1[1] <= interval2[1]):
        count = count + 1
    elif (interval2[0] <= interval1[1] and interval1[1] <= interval2[1]):
        count = count + 1

print(count)