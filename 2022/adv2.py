import sys

op = {
    'A': 'R',
    'B': 'P',
    'C': 'S'
}

me = {
    'X': 'R',
    'Y': 'P',
    'Z': 'S'
}

me_2 = {
    'X': 'L',
    'Y': 'T',
    'Z': 'W'
}

shape_score = {
    'R': 1,
    'P': 2,
    'S': 3
}

outcome_score = {
    'W': 6,
    'T': 3,
    'L': 0
}

def outcome(op_shape, my_shape):
    if(op[op_shape] == me[my_shape]):
        return 'T'
    if(op[op_shape] == 'R'):
        if(me[my_shape] == 'P'):
            return 'W'
        else:
            return 'L'
    if(op[op_shape] == 'P'):
        if(me[my_shape] == 'S'):
            return 'W'
        else:
            return 'L'
    if(op[op_shape] == 'S'):
        if(me[my_shape] == 'R'):
            return 'W'
        else:
            return 'L'

def play(op_shape, my_outcome):
    if(me_2[my_outcome] == 'T'):
        return op[op_shape]
    if(op[op_shape] == 'R'):
        if(me_2[my_outcome] == 'W'):
            return 'P'
        else:
            return 'S'
    if(op[op_shape] == 'P'):
        if(me_2[my_outcome] == 'W'):
            return 'S'
        else:
            return 'R'
    if(op[op_shape] == 'S'):
        if(me_2[my_outcome] == 'W'):
            return 'R'
        else:
            return 'P'

def score(op_shape, my_shape):
    round_outcome = outcome(op_shape, my_shape)
    round_score = shape_score[me[my_shape]] + outcome_score[round_outcome]
    return round_score
    
def score2(op_shape, my_outcome):
    my_shape = play(op_shape, my_outcome)
    round_score = shape_score[my_shape] + outcome_score[me_2[my_outcome]]
    return round_score

total = 0
for line in sys.stdin:
    op_shape, my_shape = line.strip().split(' ')
    total = total + score2(op_shape, my_shape)

print(total)