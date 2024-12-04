import sys
import json

sensor_dict = {}

def manhattan_distance(from_x, from_y, to_x, to_y):
    return abs(to_x - from_x) + abs(to_y - from_y)

def x_at_manhattan_distance(distance, from_x, from_y, to_y):
    part = distance - abs(to_y - from_y) # = abs(to_x - from_x)
    return sorted((from_x - part, from_x + part))

for line in sys.stdin:
    sensor, beacon = tuple(tuple(int(i.strip()) for i in point.strip().split(',')) for point in line.strip().split(':'))
    sensor_dict[sensor] = beacon


def remove_exclusions(intervals, y):
    exclude = list(sorted(set([sensor[0] for sensor in sensor_dict.keys() if sensor[1] == y] + [beacon[0] for beacon in sensor_dict.values() if beacon[1] == y])))
    #print("exclude", json.dumps(exclude))

    intervals_with_exclusions = []
    for exclude_x in exclude:
        if(len(intervals) == 0):
            break
        interval = intervals[0]
        intervals = intervals[1:]
        if(interval[0] == exclude_x):
            interval[0] = exclude_x + 1
            if(interval[0] > interval[1]):
                continue
            intervals = [interval] + intervals
        elif(interval[1] == exclude_x):
            interval[1] = exclude_x - 1
            if(interval[0] > interval[1]):
                continue
            intervals = [interval] + intervals
        elif(interval[0] < exclude_x and exclude_x < interval[1]):
            interval1 = (interval[0], exclude_x - 1)
            interval2 = (exclude_x + 1, interval[1])
            intervals_with_exclusions.append(interval1)
            intervals = [interval2] + intervals
        else:
            intervals_with_exclusions.append(interval)
    for remaining_interval in intervals:
        intervals_with_exclusions.append(remaining_interval)
    #print("intervals_with_exclusions", json.dumps(intervals_with_exclusions))
    return intervals_with_exclusions


def find_filled(y):
    filled = []
    for sensor, beacon in sensor_dict.items():
        sensor_beacon_distance = manhattan_distance(*sensor, *beacon)
        sensor_y_disance = manhattan_distance(*sensor, sensor[0], y)
        if(sensor_y_disance > sensor_beacon_distance):
            continue
        x_interval = x_at_manhattan_distance(sensor_beacon_distance, *sensor, y)
        #print(sensor, beacon, x_interval)
        filled.append(x_interval)

    filled = sorted(filled)
    #print("filled", json.dumps(filled))


    new_filled = []
    for curr_interval in filled:
        if(len(new_filled) == 0):
            new_filled.append(curr_interval)
            continue
        last_interval = new_filled[-1]
        new_filled = new_filled[:-1]
        if(curr_interval[0] <= last_interval[1]):
            if(curr_interval[1] > last_interval[1]):
                last_interval[1] = curr_interval[1]
            new_filled.append(last_interval)
        else:
            new_filled.append(last_interval)
            new_filled.append(curr_interval)

    #print("new_filled", json.dumps(new_filled))
    return new_filled

def part1():
    y = 10
    new_filled = find_filled(y)
    new_filled_with_exclusions = remove_exclusions(new_filled, y)

    count = 0
    for interval in new_filled_with_exclusions:
        count = interval[1] - interval[0] + 1 + count
    print(count)

def part2():
    bounds = (0, 4000001)
    x_intervals_filled = []
    for y in range(*bounds):
        #print("find_filled: ", y)
        x_intervals_filled.append(find_filled(y))

    for y in range(len(x_intervals_filled)):
        #print("find_not_filled: ", y)
        intervals = x_intervals_filled[y]
        not_filled_intervals = []
        for i in range(len(intervals) - 1):
            not_filled_intervals.append((intervals[i][1] + 1, intervals[i+1][0] - 1))
        not_filled_intervals_with_exclusions = remove_exclusions(not_filled_intervals, y)
        if(len(not_filled_intervals_with_exclusions) != 0):
            print(not_filled_intervals_with_exclusions, y)

part2()