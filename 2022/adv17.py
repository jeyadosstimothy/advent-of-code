import numpy as np
import matplotlib.pyplot as plt
import sys
import json

air_flow_offset = {
    '>': (1, 0),
    '<': (-1, 0)
}

class NegativeCoordinate(Exception):
    pass

class Rock:
    def __init__(self, coords: set[tuple[int]]):
        self.left_most = min([x for x, y in coords])
        self.right_most = max([x for x, y in coords])
        self.bottom_most = min([y for x, y in coords])
        self.top_most = max([y for x, y in coords])
        if(self.left_most < 0 or self.bottom_most < 0):
            raise NegativeCoordinate('Negatives not allowed')
        self.coords = set(coords)

    def offset(self, offset_x: int, offset_y: int):
        return Rock([(x + offset_x, y + offset_y) for x, y in self.coords])

class Cavern:
    def __init__(self, width: int, rock_spawn_offset: list[int], rocks: list[Rock], air_flow: str): 
        self.width = width
        self.rock_spawn_offset = rock_spawn_offset
        self.rocks = rocks
        self.air_flow = air_flow
        self.dp = {}

    def spawn_rock(self, rock_i: int, tallest_tower: int):
        rock_idx = rock_i % len(self.rocks)
        rock = self.rocks[rock_idx]
        spawn_offset_x, spawn_offset_y = self.rock_spawn_offset
        return rock.offset(spawn_offset_x, spawn_offset_y + tallest_tower)

    def flow_air(self, t: int, rock: Rock, stopped_rocks: set[int]):
        air_flow_at_t = self.air_flow[t % len(self.air_flow)]
        try:
            moved_rock = rock.offset(*air_flow_offset[air_flow_at_t])
        except NegativeCoordinate:
            return rock
        if(moved_rock.left_most <= 0 or moved_rock.right_most > self.width):
            return rock
        if len(moved_rock.coords.intersection(stopped_rocks)) > 0:
            return rock
        return moved_rock
    
    def can_move_down(self, rock: Rock, stopped_rocks: set[int]):
        try:
            moved_rock = rock.offset(0, -1)
        except NegativeCoordinate:
            return False
        if(moved_rock.bottom_most <= 0):
            return False
        if len(moved_rock.coords.intersection(stopped_rocks)) > 0:
            return False
        return True

    def pprint(self, t: int, rock: Rock, stopped_rocks: set[list[int]]):
        if(len(stopped_rocks) == 0):
            return
        tt = t % len(self.air_flow)
        air_flow_at_t = self.air_flow[tt]
        label = f't={t}; tt={tt}; air={air_flow_at_t}'
        plt.clf()
        plt.xlim([0, 10])
        # plt.ylim([0, 30])
        plt.scatter(*np.array(list(rock.coords)).T, c='red')
        plt.scatter(*np.array(list(stopped_rocks)).T, c='blue')
        plt.text(3, 32, label)
        plt.pause(0.05)

    def find_tallest_tower(self, num_rocks_stopped: int):
        num_rocks = 0
        tallest_tower = 0
        t = 0
        stopped_rocks = set()
        while(num_rocks < num_rocks_stopped):
            # print(num_rocks, tallest_tower, t)
            rock = self.spawn_rock(num_rocks, tallest_tower)
            if(num_rocks % len(self.rocks) == 0 and (num_rocks - 202) % 349 == 0):
                print(num_rocks, num_rocks / len(self.rocks), t, tallest_tower)
                # self.dp[t] = self.dp.get(t, 0) + 1
                # print(json.dumps(self.dp))
                # max_t_count = max([count for count in self.dp.values()])
                # self.dp = {k:v for k,v in self.dp.items() if v > max_t_count - 10}
            if(num_rocks >= 1000 and num_rocks <= 1020):
                print(num_rocks, num_rocks / len(self.rocks), t, tallest_tower)
            while True:
                # self.pprint(t, rock, stopped_rocks)
                rock = self.flow_air(t, rock, stopped_rocks)
                # self.pprint(t, rock, stopped_rocks)
                t = (t + 1) % len(self.air_flow)
                if not self.can_move_down(rock, stopped_rocks):
                    stopped_rocks = stopped_rocks.union(rock.coords)
                    tallest_tower = max(tallest_tower, rock.top_most)
                    break
                rock = rock.offset(0, -1)
            num_rocks = num_rocks + 1
        return tallest_tower



if __name__ == '__main__':
    rocks = [
        Rock([(0, 0), (1, 0), (2, 0), (3, 0)]),
        Rock([(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]),
        Rock([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
        Rock([(0, 0), (0, 1), (0, 2), (0, 3)]),
        Rock([(0, 0), (1, 0), (0, 1), (1, 1)]),
    ]

    air_flow = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

    plt.show()
    for line in sys.stdin:
        air_flow = line.strip()
        cavern = Cavern(7, (3, 4), rocks, air_flow)
        print(cavern.find_tallest_tower(1000000000000))
        break

