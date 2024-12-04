import sys

priorities = {chr(ord('a')+i): i+1 for i in range(26)}
priorities.update({chr(ord('A')+i): i+1+26 for i in range(26)})
print(priorities)

total = 0

def item_priority(sack):
    part_size = len(sack) // 2
    part1 = sack[:part_size]
    part2 = sack[part_size:]
    
    part1_set = set(part1)
    part2_set = set(part2)
    
    intersection = part1_set.intersection(part2_set)
    intersection = intersection.pop()
    return priorities[intersection]

i = 0
groups = []
for line in sys.stdin:
    i = i + 1
    groups.append(set(line.strip()))
    if(i%3 != 0):
        continue

    intersection = groups[0].intersection(groups[1])
    intersection = intersection.intersection(groups[2])
    intersection = intersection.pop()
    total = total + priorities[intersection]
    groups = []

print(total)