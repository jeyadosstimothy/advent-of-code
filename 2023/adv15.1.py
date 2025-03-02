import sys

def hash(s):
    h = 0
    for c in s:
        h = h + ord(c)
        h = h * 17
        h = h % 256
    return h

init_sequence = sys.stdin.readline().strip().split(',')

total = 0
for seq in init_sequence:
    total = total + hash(seq)
print(total)