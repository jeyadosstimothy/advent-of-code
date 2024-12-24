import re
import sys

def operate(a, b, op):
    if op == 'AND':
        return a & b
    if op == 'OR':
        return a | b
    if op == 'XOR':
        return a ^ b
    raise Exception('Unknown')


def compute(graph, wires, curr):
    if curr not in graph:
        return wires[curr]
    a, b = graph[curr]
    return operate(compute(graph, wires, a), compute(graph, wires, b), wires[curr])

if __name__ == '__main__':
    wires = dict()
    for line in sys.stdin:
        if len(line.strip()) == 0:
            break
        wire, value = line.strip().split(': ')
        wires[wire] = int(value)

    graph = dict()
    for line in sys.stdin:
        a, op, b, c = re.findall(r'(\w+) (\w+) (\w+) -> (\w+)', line.strip())[0]
        graph[c] = [a, b]
        wires[c] = op
    end_wires = list(reversed(sorted([wire for wire in wires.keys() if wire[0] == 'z'])))

    answer = 0
    for wire in end_wires:
        value = compute(graph, wires, wire)
        answer = answer << 1
        answer = answer | value
    print(answer)