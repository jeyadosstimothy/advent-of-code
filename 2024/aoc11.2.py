import math
import sys

def num_digits(stone):
    return math.floor(math.log(stone, 10)) + 1
    
def split_in_half(stone):
    digits = num_digits(stone)
    half_divisor = 10**(digits//2)
    return stone // half_divisor, stone % half_divisor

def blink(stone, times, memoized):
    if (stone, times) in memoized:
        return memoized[(stone, times)]
    if times == 0:
        memoized[(stone, times)] = 1
        return 1
    if stone == 0:
        memoized[(stone, times)] = blink(1, times - 1, memoized)
        return memoized[(stone, times)]
    if num_digits(stone) % 2 == 0:
        first, second = split_in_half(stone)
        memoized[(stone, times)] = blink(first, times - 1, memoized) + blink(second, times - 1, memoized)
        return memoized[(stone, times)]
    memoized[(stone, times)] = blink(stone * 2024, times - 1, memoized)
    return memoized[(stone, times)]

line = [int(x) for x in sys.stdin.readline().strip().split(' ')]

total = 0
memoized = dict()
for stone in line:
    total = total + blink(stone, times=75, memoized=memoized)
print(total)
