from functools import reduce
import re
import sys

schematic = []

for line in sys.stdin:
    inp = line.strip()
    schematic = schematic + [inp]

def get_surrounding_indexes(row_idx, col_begin, col_end):
    result = []
    col_left = False
    col_right = False
    if col_begin - 1 >= 0:
        col_left = True
        result.append((row_idx, col_begin - 1))
    
    if col_end < len(schematic[0]):
        col_right = True
        result.append((row_idx, col_end))

    if row_idx - 1 >= 0:
        start = col_begin - 1 if col_left else col_begin
        end = col_end + 1 if col_right else col_end
        for j in range(start, end):
            result.append((row_idx - 1, j))
    if(row_idx + 1 < len(schematic)):
        start = col_begin - 1 if col_left else col_begin
        end = col_end + 1 if col_right else col_end
        for j in range(start, end):
            result.append((row_idx + 1, j))
    return result

def is_symbol(i, j):
    return not (schematic[i][j].isdigit() or schematic[i][j] == '.')

total = 0
for i in range(len(schematic)):
    for match in re.finditer(r'[0-9]+', schematic[i]):
        surrounding_indexes = get_surrounding_indexes(i, *match.span())
        has_symbols = [is_symbol(i, j) for i,j in surrounding_indexes]
        print(has_symbols)
        has_surrounding_symbol = reduce(lambda x, y: x or y, has_symbols)
        if has_surrounding_symbol:
            total = total + int(match.group())

print(total)
