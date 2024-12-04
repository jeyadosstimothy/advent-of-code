from functools import reduce
import sys

def parse_round_info(round_info):
    return {
        cubes.strip().split(" ")[1]: int(cubes.strip().split(" ")[0])
        for cubes in round_info.split(",")
    }

def max_reducer(r1, r2):
    keys = set(list(r1.keys()) + list(r2.keys()))
    return {key: max(r1.get(key, 0), r2.get(key,0)) for key in keys}

def check_round_valid(expectation, round_info):
    keys = set(list(expectation.keys()) + list(round_info.keys()))
    for key in keys:
        e = expectation.get(key, 0)
        r = round_info.get(key, 0)
        if(r > e):
            return False
    return True

expectation = parse_round_info("12 red, 13 green, 14 blue")
print(expectation)

total = 0

for line in sys.stdin:
    game_inp = line.strip()
    game_id, game_info = game_inp.split(":")
    game_id = int(game_id.replace("Game ", ""))
    game_info = [parse_round_info(round_info) for round_info in game_info.split(";")]
    # print(game_info)
    max_cubes = reduce(max_reducer, game_info)
    # print(max_cubes)
    valid = check_round_valid(expectation, max_cubes)
    # print(valid)
    if valid:
        total = total + game_id

print(total)
