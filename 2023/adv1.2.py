import re
import sys

curr_sum = 0

m = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}
pattern = "|".join(m.keys())
rpattern = pattern[::-1]
print(pattern)
print(rpattern)
pattern = re.compile(pattern)
rpattern = re.compile(rpattern)

keywords = list(m.keys()) + list(m.values())

for line in sys.stdin:
    stripped_line = line.strip()
    front_replaced = pattern.sub(lambda y: m[y.group(0)], stripped_line, 1)
    both_replaced = rpattern.sub(lambda y: m[y.group(0)[::-1]], front_replaced[::-1], 1)[::-1]
    only_digits = re.sub(r'[^0-9]', '', both_replaced)
    num = int(only_digits[0] + only_digits[-1])
    
    min_idx = 100000000
    min_ridx = 100000000
    x = ''
    y = ''
    for kw in keywords:
        idx = stripped_line.find(kw)
        if idx != -1 and idx < min_idx:
            min_idx = idx
            x = kw if kw not in m else m[kw]
        r_idx = stripped_line[::-1].find(kw[::-1])
        if r_idx != -1 and r_idx < min_ridx:
            min_ridx = r_idx
            y = kw if kw not in m else m[kw]
    num2 = int(x) * 10 + int(y)
    print(stripped_line, only_digits, num, num2, 'yes' if num != num2 else 'no')

    curr_sum = curr_sum + num2


print(curr_sum)