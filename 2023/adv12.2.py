import sys


def possibilities(springs, damaged, dp, s=0, d=0, c=0):
    if s == len(springs):
        if d == len(damaged) or (d == len(damaged) - 1 and damaged[d] == c):
            # print(result, damaged, continuous, 'yes')
            return 1
        else:
            # print(result, damaged, continuous, 'no')
            return 0

    def handle_operational():
        nd = d
        if d < len(damaged):
            if damaged[d] == c:
                nd = d + 1
            elif c > 0:
                return 0
        return possibilities(springs, damaged, dp, s + 1, nd, 0)
    
    def handle_damaged():
        if d == len(damaged):
            return 0
        ans = possibilities(springs, damaged, dp, s + 1, d, c + 1)
        return ans

    def handle():
        if springs[s] == '.':
            return handle_operational()
        elif springs[s] == '#':
            return handle_damaged()
        elif springs[s] == '?':
            return handle_operational() + handle_damaged()
        else:
            raise Exception('unexpected character')
    
    if (s, d, c) in dp:
        return dp[(s, d, c)]
    dp[(s, d, c)] = handle()
    return dp[(s, d, c)]



total = 0
for line in sys.stdin:
    springs, damaged = line.strip().split(' ')
    damaged = list(map(int, damaged.split(',')))

    springs = '?'.join([springs] * 5)
    damaged = damaged * 5
    # print(springs, damaged)
    ans = possibilities(springs, damaged, {})
    #print(ans)
    #print()
    total = total + ans

print(total)