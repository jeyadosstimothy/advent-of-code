import sys

races = [map(int, line.strip().split(" ")) for line in sys.stdin]

total = 1
for time, highest_distance in races:
    low = (time - (time**2 - 4 * highest_distance)**0.5) // 2
    high = (time + (time**2 - 4 * highest_distance)**0.5) // 2
    while low * (time - low) <= highest_distance:
        low = low + 1
    while high * (time - high) > highest_distance:
        high = high + 1
    possible_ways = high - low
    print(low, high, possible_ways)
    total = total * possible_ways
print(total)