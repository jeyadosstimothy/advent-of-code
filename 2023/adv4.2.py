import re
import sys

count_map = {}

for line in sys.stdin:
    inp = line.strip()
    inp = re.sub(r'\s\s+', ' ', inp)
    card_info, card_numbers = inp.split(':')
    card_id = int(card_info.split(' ')[1])
    if card_id not in count_map:
        count_map[card_id] = 1
    winning_numbers, numbers_you_have = map(lambda x: set(int(n) for n in x.strip().split(' ')), card_numbers.split('|'))
    winning_numbers_you_have = winning_numbers.intersection(numbers_you_have)
    for i in range(len(winning_numbers_you_have)):
        count_map[card_id + i + 1] = count_map.get(card_id + i + 1, 1) + count_map.get(card_id, 1)

print(sum(count_map.values()))