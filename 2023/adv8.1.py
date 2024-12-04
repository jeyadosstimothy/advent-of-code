import sys
import math


instructions = "LRRLLRLRRRLRRRLRRLRRRLRRLRRRLRRLRRRLRLRRRLRRRLRRRLRLRRLRRRLRRRLRRLRRLRRLRLLLRRRLRRRLRLRLRRLLRRRLRRLRRRLRLRRLRRRLRRRLLRLRLLRRRLRRRLLRRRLRRRLRRRLRRLRRRLLLRRRLRLLLRLRLRLLRLRLLLRRLRRLLRRLRRRLRRLRRLRLRRLLRRLRLRRLLLRRRLLRRRLLRLRLLRRRLRLLRRLRLRRLRLRRRLLRRRLLRRLRLRRLRRLLRLRLRRRLRLRRRR"
instructions = [1 if x == 'R' else 0 for x in instructions]

graph = {}
for line in sys.stdin:
    inp = line.strip()
    node, edges = inp.split(" = ")
    edges = list(edges[1:-1].split(', '))
    graph[node] = edges

start = 'AAA'

step = 0
curr = start
while curr != 'ZZZ':
    curr = graph[curr][instructions[step % len(instructions)]]
    step = step + 1
print(step)