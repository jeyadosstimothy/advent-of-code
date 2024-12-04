import sys

def valid(levels):
    is_increasing, is_decreasing = True, True
    for i in range(1, len(levels)):
        if levels[i-1] < levels[i] and levels[i] - levels[i-1] <= 3:
            continue
        is_increasing = False

    for i in range(1, len(levels)):
        if levels[i-1] > levels[i] and levels[i-1] - levels[i] <= 3:
            continue
        is_decreasing = False

    return is_increasing or is_decreasing

valid_reports = 0
for line in sys.stdin:
    levels = [int(x) for x in line.strip().split(' ')]

    if valid(levels):
        valid_reports = valid_reports + 1
        continue

    for i in range(len(levels)):
        if valid(levels[:i] + levels[i+1:]):
            valid_reports = valid_reports + 1
            break

print(valid_reports)
