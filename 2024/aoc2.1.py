import sys

valid_reports = 0
for line in sys.stdin:
    levels = [int(x) for x in line.strip().split(' ')]
    is_increasing, is_decreasing = True, True
    for i in range(1, len(levels)):
        if levels[i-1] < levels[i] and levels[i] - levels[i-1] <= 3:
            continue
        is_increasing = False

    for i in range(1, len(levels)):
        if levels[i-1] > levels[i] and levels[i-1] - levels[i] <= 3:
            continue
        is_decreasing = False

    if is_increasing or is_decreasing:
        valid_reports = valid_reports + 1

print(valid_reports)
