import sys

clock = 0
total = 0
register = 1
screen = ''

for line in sys.stdin:
    command = line.strip().split(' ')
    to_add = 0
    if(command[0] == 'noop'):
        duration = 1
    else:
        to_add = int(command[1])
        duration = 2
    while(duration != 0):
        position = clock % 40
        print(clock, position, register)
        if(position == 0):
            screen = screen + '\n'
        if(register - 1 <= position and position <= register + 1):
            screen = screen + '#'
        else:
            screen = screen + '.'

        duration = duration - 1
        clock = clock + 1
        
        if((clock + 20) % 40 == 0):
            total = total + register * clock

    register = register + to_add

print(total)
print(screen)