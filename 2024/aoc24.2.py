import re
import sys

def get_from_input(gates, a, b, op, expected=None):
    if (a, op, b) in gates:
        actual = gates[(a, op, b)]
        if expected is not None:
            assert_equals(expected, actual)
        return actual
    if (b, op, a) in gates:
        actual = gates[(b, op, a)]
        if expected is not None:
            assert_equals(expected, actual)
        return actual
    raise Exception(f'not found: {a} {op} {b}')

def assert_equals(expected, actual):
    if expected != actual:
        raise Exception(f'expected != actual: {expected} != {actual}')

def get_xyz(n):
    return [f'{s}{n:02d}' for s in 'xyz']

def validate(gates):
    graph = dict()
    for i in range(45):
        print(i)
        xi, yi, zi = get_xyz(i)
        if i == 0:
            s = get_from_input(gates, xi, yi, 'XOR', expected=zi)
        elif i == 1:
            s = get_from_input(gates, xi, yi, 'XOR')
            x0, y0, z0 = get_xyz(0)
            c = get_from_input(gates, x0, y0, 'AND')
            z_actual = get_from_input(gates, s, c, 'XOR', expected=zi)
            graph[('s', i)] = s
            graph[('c', i)] = c
        else:
            s = get_from_input(gates, xi, yi, 'XOR')
            xm, ym, zm = get_xyz(i - 1)
            ca = get_from_input(gates, xm, ym, 'AND')
            cb = get_from_input(gates, graph[('s', i - 1)], graph[('c', i - 1)], 'AND')
            c = get_from_input(gates, ca, cb, 'OR')
            z_actual = get_from_input(gates, s, c, 'XOR', expected=zi)
            graph[('s', i)] = s
            graph[('c', i)] = c
        i = i + 1


if __name__ == '__main__':
    inputs = dict()
    for line in sys.stdin:
        if len(line.strip()) == 0:
            break
        wire, value = line.strip().split(': ')
        inputs[wire] = int(value)

    gates = dict()
    for line in sys.stdin:
        a, op, b, c = re.findall(r'(\w+) (\w+) (\w+) -> (\w+)', line.strip())[0]
        gates[(a, op, b)] = c

    validate(gates)
