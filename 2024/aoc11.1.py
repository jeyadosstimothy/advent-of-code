import math
import sys
import time

def num_digits(value):
    return math.floor(math.log(value, 10)) + 1
    
def split_in_half(value):
    digits = num_digits(value)
    half_divisor = 10**(digits//2)
    return value // half_divisor, value % half_divisor

def blink(stones):
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
            continue

        if num_digits(stone) % 2 == 0:
            new_stones.extend(split_in_half(stone))
            continue

        new_stones.append(stone * 2024)
    return new_stones

stones = [int(x) for x in sys.stdin.readline().strip().split(' ')]

for i in range(75):
    stones = blink(stones)
    print(len(stones))
    
