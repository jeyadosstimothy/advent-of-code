import sys

def can_make(expectation, operands, idx = 0, current = 0):
    # print(f'expectation: {expectation}, operands: {operands}, idx: {idx}, current: {current}')
    if idx == len(operands):
        return expectation == current
    if idx == 0:
        return can_make(expectation, operands, idx + 1, operands[idx])
    if current > expectation:
        return False
    can_make_via_addition = can_make(expectation, operands, idx + 1, current + operands[idx])
    can_make_via_multiplication = can_make(expectation, operands, idx + 1, current * operands[idx])
    can_make_via_concatenation = can_make(expectation, operands, idx + 1, int(str(current) + str(operands[idx])))
    return can_make_via_addition or can_make_via_multiplication or can_make_via_concatenation

total = 0
for line in sys.stdin:
    inp = line.strip()
    expectation, operands = inp.split(': ')
    expectation = int(expectation)
    operands = [int(x) for x in operands.split(' ')]
    if can_make(expectation, operands):
        print('can make')
        total = total + expectation
    else:
        print('cannot make')

print(total)
