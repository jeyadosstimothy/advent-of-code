import sys

signal_pairs = [[]]
score = 0


def is_in_order(a, b):
    if(isinstance(a, list)):
        if(isinstance(b, list)):
            for i in range(len(a)):
                if(i >= len(b)):
                    return 1
                result = is_in_order(a[i], b[i])
                if(result is not None):
                    return result
            if(len(a) < len(b)):
                return -1
            else:
                return 0
        else:
            return is_in_order(a, [b])
    else:
        if(isinstance(b, list)):
            return is_in_order([a], b)
        else:
            if(a < b):
                return -1
            elif(a > b):
                return 1
            else:
                return 0


for line in sys.stdin:
    if(len(line.strip()) == 0):
        a, b = signal_pairs[-1][0], signal_pairs[-1][1]
        exec('a = ' + a)
        exec('b = '+ b)
        if(is_in_order(a, b)):
            score = score + len(signal_pairs)
        signal_pairs.append([])
    else:
        signal_pairs[-1].append(line.strip())

print(score)

all_signals = [[[2]], [[6]]]

for pair in signal_pairs:
    a, b = pair
    exec('a = ' + a)
    exec('b = ' + b)
    all_signals.append(a)
    all_signals.append(b)

import functools

sorted_signals = sorted(all_signals, key=functools.cmp_to_key(is_in_order))

for signal in sorted_signals:
    print(signal)

index2 = sorted_signals.index([[2]]) + 1
index6 = sorted_signals.index([[6]]) + 1
print(index2 * index6)
