import math
import sys
import time

class Stone:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None
    
    def __repr__(self):
        return str(self.value)

def num_digits(value):
    return math.floor(math.log(value, 10)) + 1
    
def split_number_in_half(value):
    digits = num_digits(value)
    half_divisor = 10**(digits//2)
    return value // half_divisor, value % half_divisor

class Line:
    def __init__(self, stones):
        self.head, self.tail = Line.connect_stones(stones)

    def __repr__(self):
        stones = []
        head = self.head
        while head is not None:
            stones.append(head.value)
            head = head.next
        return str(stones)
    
    def __len__(self):
        size = 0
        head = self.head
        while head is not None:
            size = size + 1
            head = head.next
        return size

    def connect_stones(stones):
        prev = None
        next = None
        for i in range(len(stones)):
            stones[i].prev = prev
            prev = stones[i]
            stones[len(stones) - i - 1].next = next
            next = stones[len(stones) - i - 1]
        return stones[0], stones[-1]

    def add_stone(stone, new_stone):
        next_stone = stone.next
        new_stone.prev = stone
        new_stone.next = next_stone
        stone.next = new_stone
        if next_stone is not None:
            next_stone.prev = new_stone
        return new_stone

    def blink(self):
        head = self.head
        while head is not None:
            if head.value == 0:
                head.value = 1
                head = head.next
                continue

            if num_digits(head.value) % 2 == 0:
                first, second = split_number_in_half(head.value)
                head.value = first
                new_stone = Line.add_stone(head, Stone(second))
                head = new_stone.next
                continue

            head.value = head.value * 2024
            head = head.next

line = Line([Stone(int(x)) for x in sys.stdin.readline().strip().split(' ')])

for i in range(25):
    line.blink()
    print(len(line))
