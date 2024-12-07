import sys

def can_make(expectation, operands):
    if len(operands) == 0:
        return expectation == 0

    last_operand = operands[-1]

    can_make_via_addition = False
    if expectation > last_operand:
        can_make_via_addition = can_make(expectation - last_operand, operands[:-1])

    can_make_via_multiplication = False
    if expectation % last_operand == 0:
        can_make_via_multiplication = can_make(expectation // last_operand, operands[:-1])

    can_make_via_concatenation = False
    last_operand_str = str(last_operand)
    expectation_str = str(expectation)
    if expectation_str[-len(last_operand_str):] == last_operand_str:
        updated_expectation = expectation_str[:-len(last_operand_str)]
        can_make_via_concatenation = can_make(0 if updated_expectation == '' else int(updated_expectation), operands[:-1])

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
