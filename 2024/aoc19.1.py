import sys

def possible(towels, design, done=0):
    if done == len(design):
        return True
    print(done)
    for i in range(done+1, len(design)+1):
        print(i, design[done:i])
        if design[done:i] in towels and possible(towels, design, i):
            return True
    return False

if __name__ == '__main__':
    towels = set(sys.stdin.readline().strip().split(', '))
    sys.stdin.readline()
    designs = [line.strip() for line in sys.stdin]
    print(towels)
    print(designs)

    total = 0
    for design in designs:
        print(f"finding {design}")
        if possible(towels, design):
            total = total + 1
    print(total)
    
