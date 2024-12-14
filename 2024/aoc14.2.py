from pprint import pprint
import sys
import matplotlib.pyplot as plt
import numpy as np


def print_graph(title, positions, nx, ny):
    print(title)
    for j in range(ny):
        row = ''
        for i in range(nx):
            if (i, j) in positions:
                row = row + '#'
            else:
                row = row + ' '
        print(row)

def plot_graph(title, positions, nx, ny):
    x, y = [i for (_, i) in positions], [i for (i, _) in positions]
    xpoints = np.array(x)
    ypoints = np.array(y)
    plt.plot(xpoints, ypoints, 'o')
    plt.title(title)
    plt.show()

if __name__ == '__main__':
    nx, ny = 101, 103

    robots = []
    for line in sys.stdin:
        (px, py), (vx, vy) = map(lambda s: map(int, s.split('=')[1].split(',')), line.strip().split(' '))
        robots.append(((px, py), (vx, vy)))

    iter = [31, 88] # 134, 189, 237, 290

    for i in range(1, 100):
        iter.append(iter[0] + i * ny)
        iter.append(iter[1] + i * nx)

    for i in iter:
        positions = set()
        for (px, py), (vx, vy) in robots:
            fx, fy = (px + i * vx) % nx, (py + i * vy) % ny
            positions.add((fx, fy))
        plot_graph(f'Iter: {i}', positions, nx, ny)

