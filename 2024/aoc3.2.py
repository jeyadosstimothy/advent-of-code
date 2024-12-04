import re
import sys

mul_pattern = re.compile(r'mul\((\d+),(\d+)\)')
disabled_pattern_1 = re.compile(r'don\'t\(\).*?do\(\)')
disabled_pattern_2 = re.compile(r'don\'t\(\).*$')

inp = ''.join(line.strip() for line in sys.stdin)
inp = disabled_pattern_1.sub('', inp)
inp = disabled_pattern_2.sub('', inp)

total = 0
for a, b in mul_pattern.findall(inp):
    total = total + int(a) * int(b)
print(total)
