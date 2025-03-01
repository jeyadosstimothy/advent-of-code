import sys


def possibilities(springs, damaged, continuous=0, result=''):
    if len(springs) == 0:
        if len(damaged) == 0 or (len(damaged) == 1 and damaged[0] == continuous):
            # print(result, damaged, continuous, 'yes')
            return 1
        else:
            # print(result, damaged, continuous, 'no')
            return 0

    def handle_operational():
        new_damaged = damaged
        if len(damaged) > 0:
            if damaged[0] == continuous:
                new_damaged = damaged[1:]
            elif continuous > 0:
                return 0
        return possibilities(springs[1:], new_damaged, 0, result + '.')
    
    def handle_damaged():
        if len(damaged) == 0:
            return 0
        ans = possibilities(springs[1:], damaged, continuous + 1, result + '#')
        return ans

    if springs[0] == '.':
        return handle_operational()
    elif springs[0] == '#':
        return handle_damaged()
    elif springs[0] == '?':
        return handle_operational() + handle_damaged()
    else:
        raise Exception('unexpected character')



total = 0
for line in sys.stdin:
    springs, damaged = line.strip().split(' ')
    damaged = list(map(int, damaged.split(',')))
    # print(springs, damaged)
    ans = possibilities(springs, damaged)
    #print(ans)
    #print()
    total = total + ans

print(total)