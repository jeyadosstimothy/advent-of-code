import re
import sys

total = 0

for line in sys.stdin:
    inp = line.strip()
    inp = re.sub(r'\s\s+', ' ', inp)
    card_info, card_numbers = inp.split(':')
    card_id = int(card_info.split(' ')[1])
    winning_numbers, numbers_you_have = map(lambda x: set(int(n) for n in x.strip().split(' ')), card_numbers.split('|'))
    winning_numbers_you_have = winning_numbers.intersection(numbers_you_have)
    points = 0 if len(winning_numbers_you_have) == 0 else 2**(len(winning_numbers_you_have) - 1) 
    total = total + points    

print(total)