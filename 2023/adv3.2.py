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
    
    if col_end < len(schematic[row_idx]):
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

def find_all_digits(i, j):
    left = ''
    right = ''
    start = j
    end = j
    for k in range(j - 1, -1, -1):
        if schematic[i][k].isdigit():
            left = left + schematic[i][k]
            start = k
        else:
            break
    for k in range(j + 1, len(schematic[i])):
        if schematic[i][k].isdigit():
            right = right + schematic[i][k]
            end = k
        else:
            break
    return (i, start, end + 1), int(left[::-1] + schematic[i][j] + right)

total = 0
for i in range(len(schematic)):
    for match in re.finditer(r'\*', schematic[i]):
        surrounding_indexes = get_surrounding_indexes(i, *match.span())
        numbers = dict(find_all_digits(i,j) for i,j in surrounding_indexes if schematic[i][j].isdigit())
        print(numbers)
        numbers = list(numbers.values())
        if len(numbers) == 2:
            total = total + numbers[0] * numbers[1]

print(total)
