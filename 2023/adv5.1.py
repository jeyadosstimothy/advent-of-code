import bisect
import re
import sys
import jsonpickle


class Almanac:
    def __init__(self):
        self.entries = []

    def add(self, source_start, dest_start, count):
        entry = {"source_start": source_start, "dest_start": dest_start, "count": count}
        bisect.insort(self.entries, entry, key=lambda x: x["source_start"])

    def _find_entry(self, number):
        "Find rightmost value less than or equal to number"
        i = bisect.bisect_right(self.entries, number, key=lambda x: x["source_start"])
        if i:
            return self.entries[i - 1]
        return None

    def map_number(self, number):
        entry = self._find_entry(number)
        if entry is None:
            return number

        source_start, dest_start, count = (
            entry["source_start"],
            entry["dest_start"],
            entry["count"],
        )
        if number > source_start + count:
            return number

        return dest_start + number - source_start


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

result = []
for seed in seeds:
    curr = "seed"
    number = seed
    while curr in path:
        almanac = almanacs[curr]
        number = almanac.map_number(number)
        curr = path[curr]
    result.append(number)

print(sorted(result)[0])
