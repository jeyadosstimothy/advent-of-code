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

start = [node for node in graph if node[-1] == 'A']

step = 0
curr = start
first_reach_steps = [-1] * len(curr)
while set(x[-1] for x in curr) != set('Z'):
    curr = [graph[node][instructions[step % len(instructions)]] for node in curr]
    step = step + 1
    result = [step if x[-1] == 'Z' else -1 for x in curr]
    if result != [-1] * len(curr):
        first_reach_steps = [max(x,y) for x, y in zip(first_reach_steps, result)]
    if -1 not in first_reach_steps:
        break
print(first_reach_steps)
print(math.lcm(*first_reach_steps))