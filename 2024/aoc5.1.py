import sys
from functools import cmp_to_key


orders = dict()
for line in sys.stdin:
    inp = line.strip()
    if len(inp) == 0:
        break
    a, b = (int(x) for x in inp.split('|'))
    orders[a] = orders.get(a, []) + [b]

def compare(x, y):
    if x in orders and y in orders[x]:
        # x < y
        return -1

    if y in orders and x in orders[y]:
        # x > y
        return 1
    return 0

total = 0
for line in sys.stdin:
    inp = line.strip()
    row = [int(x) for x in inp.split(',')]
    sorted_row = sorted(row, key=cmp_to_key(compare))
    if row == sorted_row:
        print(row, 'correct')
        middle = row[len(row)//2]
        total = total + middle
    else:
        print(row, 'incorrect')

print(total)
