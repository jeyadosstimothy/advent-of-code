import sys

def possible(towels, design, memoized=dict(), done=0):
    if done == len(design):
        memoized[done] = 1
        return 1
    if done in memoized:
        return memoized[done]
    count = 0
    for i in range(done+1, len(design)+1):
        print(i, design[done:i])
        if design[done:i] in towels:
            count = count + possible(towels, design, memoized, i)
    memoized[done] = count
    return count

if __name__ == '__main__':
    towels = set(sys.stdin.readline().strip().split(', '))
    sys.stdin.readline()
    designs = [line.strip() for line in sys.stdin]
    print(towels)
    print(designs)

    total = 0
    for design in designs:
        print(f"finding {design}")
        memoized=dict()
        total = total + possible(towels, design, memoized)
        print(memoized)
    print(total)
    
