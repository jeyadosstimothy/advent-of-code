import bisect
import re
import sys
import jsonpickle


class AlmanacEntry:
    def __init__(self, source_start, dest_start, count):
        self.source_start = source_start
        self.dest_start = dest_start
        self.count = count

    def __repr__(self):
        return f'(source_start: {self.source_start}, dest_start: {self.dest_start}, count: {self.count})'

class Almanac:
    def __init__(self):
        self.entries = []

    def add(self, source_start, dest_start, count):
        bisect.insort(
            self.entries,
            AlmanacEntry(source_start, dest_start, count),
            key=lambda x: x.source_start,
        )

    def map_number(self, number):
        i = bisect.bisect_right(self.entries, number, key=lambda x: x.source_start)
        if not i:
            return number
        entry = self.entries[i - 1]
        if number > entry.source_start + entry.count:
            return number

        return entry.dest_start + number - entry.source_start

    def map_range(self, start, count):
        result_ranges = []
        curr = start
        i = bisect.bisect_right(self.entries, curr, key=lambda x: x.source_start)
        if i:
            i = i - 1
        if not i:
            i = 0
        while count != 0:
            if i == len(self.entries):
                result_ranges.append((curr, count))
                curr = curr + count
                count = 0
                break

            entry = self.entries[i]
            
            if entry.source_start + entry.count < curr:
                i = i + 1
                continue
            
            if curr < entry.source_start:
                result_count = min(entry.source_start - curr, count)
                result_ranges.append((curr, result_count))
                curr = curr + result_count
                count = count - result_count
                continue

            if curr <= entry.source_start + entry.count:
                diff_to_curr = curr - entry.source_start
                result_start = entry.dest_start + diff_to_curr
                result_count = min(count, entry.count - diff_to_curr)
                result_ranges.append((result_start, result_count))
                curr = curr + result_count
                count = count - result_count
                i = i + 1
                continue

            print("loop shouldn't come here")
            break

        return result_ranges


seeds = []
almanacs = dict()
path = dict()


curr_inp_section = None
for line in sys.stdin:
    inp = line.strip()
    if len(inp) == 0:
        curr_inp_section = ""
        continue
    if ":" in inp:
        curr_inp_section = list(inp[:-1].split("-"))
        if len(curr_inp_section) == 2:
            source, dest = curr_inp_section
            path[source] = dest
        continue
    if curr_inp_section == ["seeds"]:
        seeds = [int(x) for x in inp.split(" ")]
        continue
    source, dest = curr_inp_section
    dest_start, source_start, count = map(int, inp.split(" "))
    almanac = almanacs.get(source, Almanac())
    almanac.add(source_start, dest_start, count)
    almanacs[source] = almanac


full_result_ranges = []
for seed_start, seed_count in zip(seeds[::2], seeds[1::2]):
    curr = "seed"
    result_ranges = [(seed_start, seed_count)]
    while curr in path:
        almanac = almanacs[curr]
        mapped_result_ranges = []
        for start, count in result_ranges:
            mapped_results = almanac.map_range(start, count)
            mapped_result_ranges.extend(mapped_results)
        result_ranges = mapped_result_ranges
        curr = path[curr]
    full_result_ranges.extend(result_ranges)

print(sorted(full_result_ranges)[0])
