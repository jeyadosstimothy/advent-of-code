import sys

def find_next_elem(series):
    if series == [0] * len(series):
        return 0
    diff_series = []
    for i in range(len(series) - 1):
        diff_series.append(series[i + 1] - series[i])
    return series[-1] + find_next_elem(diff_series)

def find_prev_elem(series):
    if series == [0] * len(series):
        return 0
    diff_series = []
    for i in range(len(series) - 1):
        diff_series.append(series[i + 1] - series[i])
    return series[0] - find_prev_elem(diff_series)

total = 0
for line in sys.stdin:
    series = list(map(int, line.strip().split(' ')))
    next = find_next_elem(series)
    total = total + next

print(total)
    

