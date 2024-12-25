import sys

if __name__ == '__main__':
    locks, keys = [], []
    lock_or_key = []
    for line in sys.stdin:
        if len(line.strip()) == 0:
            if set(lock_or_key[0]) == set(['#']):
                locks.append(lock_or_key)
            if set(lock_or_key[0]) == set(['.']):
                keys.append(lock_or_key)
            lock_or_key = []
            continue
        lock_or_key.append(line.strip())
    if set(lock_or_key[0]) == set(['#']):
        locks.append(lock_or_key)
    if set(lock_or_key[0]) == set(['.']):
        keys.append(lock_or_key)

    lock_heights = []
    for lock in locks:
        heights = []
        for j in range(len(lock[0])):
            height = 0
            for i in range(1, len(lock)):
                if lock[i][j] == '#':
                    height = height + 1
            heights.append(height)
        lock_heights.append(heights)
    
    key_heights = []
    for key in keys:
        heights = []
        for j in range(len(key[0])):
            height = 0
            for i in range(len(key) - 1):
                if key[i][j] == '#':
                    height = height + 1
            heights.append(height)
        key_heights.append(heights)
    
    total = 0
    for lock in lock_heights:
        for key in key_heights:
            fit = True
            for i in range(len(lock)):
                if lock[i] + key[i] > 5:
                    fit = False
            if fit:
                total = total + 1
    print(total)
