import sys
from functools import cmp_to_key

card_order = ['J','2','3','4','5','6','7','8','9','T','Q','K','A']

def compare_cards(a, b):
    index_a = card_order.index(a)
    index_b = card_order.index(b)
    if(index_a < index_b):
        return -1 
    if(index_a > index_b):
        return 1
    return 0 

def compare_card_count(a, b):
    if a[1] < b[1]:
        return -1
    if a[1] > b[1]:
        return 1
    return compare_cards(a[0], b[0])

def get_hand_type(hand):
    hand_type = {x: hand.count(x) for x in hand}
    if 'J' in hand_type and hand_type['J'] != 5:
        joker_count = hand_type['J']
        del hand_type['J']
        print(hand, hand_type)
        most_repeated_card, most_repeated_count = sorted(hand_type.items(), key=cmp_to_key(compare_card_count), reverse=True)[0]
        hand_type[most_repeated_card] = most_repeated_count + joker_count
    return hand_type

def compare_hands(a, b):
    hand_a = a[0]
    hand_b = b[0]
    hand_type_a = get_hand_type(hand_a)
    hand_type_b = get_hand_type(hand_b)

    if len(hand_type_a) > len(hand_type_b):
        return -1
    if len(hand_type_a) < len(hand_type_a):
        return 1
    
    hand_type_values_a = sorted(hand_type_a.values(), reverse=True)
    hand_type_values_b = sorted(hand_type_b.values(), reverse=True)
    if hand_type_values_a < hand_type_values_b:
        return -1
    if hand_type_values_a > hand_type_values_b:
        return 1

    for x, y in zip(hand_a, hand_b):
        card_result = compare_cards(x, y)
        if card_result == 0:
            continue
        return card_result

    return 0

hands = [line.strip().split(" ") for line in sys.stdin]

sorted_hands = sorted(hands, key=cmp_to_key(compare_hands))

total = 0
for i in range (len(sorted_hands)):
    total = total + int(sorted_hands[i][1]) * (i + 1)
print(sorted_hands)
print(total)