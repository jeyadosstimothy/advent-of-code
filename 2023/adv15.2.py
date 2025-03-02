import sys

def hash(s):
    h = 0
    for c in s:
        h = h + ord(c)
        h = h * 17
        h = h % 256
    return h

init_sequence = sys.stdin.readline().strip().split(',')

boxes = {}

for seq in init_sequence:
    if '=' in seq:
        label, focal_length = seq.split('=')
        focal_length = int(focal_length)
        box_num = hash(label)
        lenses = boxes.get(box_num, [])
        already_present = False
        for lens in lenses:
            if lens[0] == label and not lens[2]:
                already_present = True
                lens[1] = focal_length
                break
        if not already_present:
            lenses.append([label, focal_length, False])
        boxes[box_num] = lenses
    if '-' in seq:
        label, _ = seq.split('-')
        box_num = hash(label)
        lenses = boxes.get(box_num, [])
        for lens in lenses:
            if lens[0] == label and not lens[2]:
                lens[2] = True
                break
        boxes[box_num] = lenses

for box_num in boxes:
    boxes[box_num] = [lens for lens in boxes[box_num] if not lens[2]]
# print(boxes)

total = 0
for box_num in boxes:
    for i in range(len(boxes[box_num])):
        focusing_power = (1 + box_num) * (i + 1) * boxes[box_num][i][1]
        # print(box_num, i, focusing_power)
        total = total + focusing_power
print(total)