def test(a):
    # Equivalent to 2,4,1,5,7,5,1,6,0,3,4,3,5,5,3,0
    while a != 0:
        b = 3 ^ (a % 8) ^ (a >> ((a % 8) ^ 5))
        a = a >> 3
        print(b % 8, end = ',')

# reverse engineer the test function
def solve(program, i=0, a=0):
    if i == len(program):
        return set([a])
    solutions = set()
    for aa in range(8):
        new_a = (a << 3) | aa
        b = (3 ^ aa ^ (new_a >> (aa ^ 5))) % 8
        # print(i, new_a, aa, b, program[i])
        if b == program[i]:
            solutions.update(solve(program, i + 1, new_a))
    return solutions

if __name__ == '__main__':
    program = list(map(int,'2,4,1,5,7,5,1,6,0,3,4,3,5,5,3,0'.split(',')))
    print(len(program))
    solutions = set()
    for i in range(8):
        solutions.update(solve(list(reversed(program))))
    print(solutions)
    answer = min(solutions)
    print(answer)
    test(answer)