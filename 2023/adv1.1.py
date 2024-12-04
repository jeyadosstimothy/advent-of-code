import re
import sys

curr_sum = 0

for line in sys.stdin:
    x = line.strip()
    x = re.sub(r'[^0-9]', '', x)
    x = int(x[0] + x[-1])
    curr_sum = curr_sum + x

print(curr_sum)