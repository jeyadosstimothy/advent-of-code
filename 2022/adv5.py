#                 [M]     [V]     [L]
# [G]             [V] [C] [G]     [D]
# [J]             [Q] [W] [Z] [C] [J]
# [W]         [W] [G] [V] [D] [G] [C]
# [R]     [G] [N] [B] [D] [C] [M] [W]
# [F] [M] [H] [C] [S] [T] [N] [N] [N]
# [T] [W] [N] [R] [F] [R] [B] [J] [P]
# [Z] [G] [J] [J] [W] [S] [H] [S] [G]
#  1   2   3   4   5   6   7   8   9 
import sys 

all_crates = { k: list(v) for k, v in {
    1: 'GJWRFTZ',
    2: 'MWG',
    3: 'GHNJ',
    4: 'WNCRJ',
    5: 'MVQGBSFW',
    6: 'CWVDTRS',
    7: 'VGZDCNBH',
    8: 'CGMNJS',
    9: 'LDJCWNPG'
}.items()}

for line in sys.stdin:
    n, a, b = [int(x) for x in line.strip().split(' ')]

    a_crates = all_crates[a]
    b_crates = all_crates[b]

    move_crates = a_crates[:n]
    a_crates = a_crates[n:]
    b_crates = list(move_crates) + b_crates
    all_crates[a] = a_crates
    all_crates[b] = b_crates

print(''.join([v[0] for k, v in all_crates.items()]))