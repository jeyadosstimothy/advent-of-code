monkeys = [
    {
        'items': [54, 82, 90, 88, 86, 54],
        'operation': lambda x: x * 7,
        'test': {
            'divisor': 11,
            'true': 2,
            'false': 6
        },
        'inspections': 0
    },
    {
        'items': [91, 65],
        'operation': lambda x: x * 13,
        'test': {
            'divisor': 5,
            'true': 7,
            'false': 4
        },
        'inspections': 0
    },
    {
        'items': [62, 54, 57, 92, 83, 63, 63],
        'operation': lambda x: x + 1,
        'test': {
            'divisor': 7,
            'true': 1,
            'false': 7
        },
        'inspections': 0
    },
    {
        'items': [67, 72, 68],
        'operation': lambda x: x * x,
        'test': {
            'divisor': 2,
            'true': 0,
            'false': 6
        },
        'inspections': 0
    },
    {
        'items': [68, 89, 90, 86, 84, 57, 72, 84],
        'operation': lambda x: x + 7,
        'test': {
            'divisor': 17,
            'true': 3,
            'false': 5
        },
        'inspections': 0
    },
    {
        'items': [79, 83, 64, 58],
        'operation': lambda x: x + 6,
        'test': {
            'divisor': 13,
            'true': 3,
            'false': 0
        },
        'inspections': 0
    },
    {
        'items': [96, 72, 89, 70, 88],
        'operation': lambda x: x + 4,
        'test': {
            'divisor': 3,
            'true': 1,
            'false': 2
        },
        'inspections': 0
    },
    {
        'items': [79],
        'operation': lambda x: x + 8,
        'test': lambda x: 4 if x % 19 == 0 else 5,
        'test': {
            'divisor': 19,
            'true': 4,
            'false': 5
        },
        'inspections': 0
    }
]

from math import prod
gcd = prod(x['test']['divisor'] for x in monkeys)

for round in range(10000):
    print('Round ', round)
    for monkey in monkeys:
        for item in monkey['items']:
            new_item = monkey['operation'](item)
            new_item = new_item % gcd
            dest_monkey_idx = monkey['test']['true'] if new_item % monkey['test']['divisor'] == 0 else monkey['test']['false']
            monkeys[dest_monkey_idx]['items'].append(new_item)
            monkey['inspections'] = monkey['inspections'] + 1
        monkey['items'] = []

a, b = sorted([monkey['inspections'] for monkey in monkeys])[-2:]
print(a * b)