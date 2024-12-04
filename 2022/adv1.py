import sys

curr_sum = 0
max_sum = [0]

for line in sys.stdin:
    if(line != '\n'):
        curr = int(line)
        curr_sum = curr_sum + curr
        max_sum = max_sum + [curr_sum]
        max_sum = sorted(max_sum)
        max_sum = max_sum[-3:]
    else:
        curr_sum = 0

print(max_sum)
print(sum(max_sum))