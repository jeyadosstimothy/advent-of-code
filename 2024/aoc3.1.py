import re
import sys

pattern = re.compile(r'mul\((\d+),(\d+)\)')

total = 0
for line in sys.stdin:
    inp = line.strip()
    for a, b in pattern.findall(inp):
        total = total + int(a) * int(b)

print(total)
