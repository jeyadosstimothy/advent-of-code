from pprint import pprint
import sys

def print_graph(positions, nx, ny):
    graph = []
    for j in range(ny):
        row = []
        for i in range(nx):
            row.append(positions.get((i, j), '.'))
        graph.append(row)
    pprint(graph)

def find_total(positions, nx, ny):
    hnx, hny = nx // 2, ny // 2

    q1, q2, q3, q4 = 0, 0, 0, 0
    for x, y in positions:
        if 0 <= x and x < hnx and 0 <= y and y < hny:
            q1 = q1 + positions[(x, y)]
        elif 0 <= x and x < hnx and hny < y and y < ny:
            q2 = q2 + positions[(x, y)]
        elif hnx < x and x < nx and 0 <= y and y < hny:
            q3 = q3 + positions[(x, y)]
        elif hnx < x and x < nx and hny < y and y < ny:
            q4 = q4 + positions[(x, y)]
        else:
            continue
    print(f'q1, q2, q3, q4: {q1, q2, q3, q4}')
    return q1 * q2 * q3 * q4

if __name__ == '__main__':
    nx, ny = 101, 103

    positions = dict()
    for line in sys.stdin:
        (px, py), (vx, vy) = map(lambda s: map(int, s.split('=')[1].split(',')), line.strip().split(' '))

        fx, fy = (px + 100 * vx) % nx, (py + 100 * vy) % ny
        print(f'px, py: ({px, py}), vx, vy: ({vx, vy}), fx, fy: ({fx, fy})')
        positions[(fx, fy)] = positions.get((fx, fy), 0) + 1

    print_graph(positions, nx, ny)
    print(find_total(positions, nx, ny))