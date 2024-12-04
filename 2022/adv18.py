import sys

class SameCube(Exception):
    pass

class TooManyCommonSurfaces(Exception):
    pass

cube_coords = []
surfaces = set()
surface_offsets = [
    [(0, 0, 0), (0, -1, 0), (-1, -1, 0), (-1, 0, 0)],
    [(0, 0, -1), (0, -1, -1), (-1, -1, -1), (-1, 0, -1)],
    [(0, 0, 0), (0, 0, -1), (0, -1, -1), (0, -1, 0)],
    [(-1, 0, 0), (-1, 0, -1), (-1, -1, -1), (-1, -1, 0)],
    [(0, 0, 0), (0, 0, -1), (-1, 0, -1), (-1, 0, 0)],
    [(0, -1, 0), (0, -1, -1), (-1, -1, -1), (-1, -1, 0)]
]

def get_surfaces(x: int, y: int, z: int) -> set[int]:
    return set(tuple(sorted((x + offset_x, y + offset_y, z + offset_z) for offset_x, offset_y, offset_z in surface_offset)) for surface_offset in surface_offsets)

def get_common_surfaces(cube1: list[int], cube2: list[int]) -> list[int]:
    if(cube1 == cube2):
        raise SameCube()
    cube1_surfaces = get_surfaces(*cube1)
    cube2_surfaces = get_surfaces(*cube2)
    common_surfaces = cube1_surfaces.intersection(cube2_surfaces)
    if(len(common_surfaces) > 1):
        raise TooManyCommonSurfaces()
    return list(common_surfaces)

for line in sys.stdin:
    x, y, z = [int(i) for i in line.strip().split(',')]
    cube_coords.append((x, y, z))

for x, y, z in cube_coords:
    new_surfaces = get_surfaces(x, y, z)
    common_surfaces = surfaces.intersection(new_surfaces)
    surfaces = surfaces.union(new_surfaces)
    surfaces = surfaces.difference(common_surfaces)

print(len(surfaces))


min_x = min([x for side in surfaces for x, y, z in side]) - 1
max_x = max([x for side in surfaces for x, y, z in side]) + 1
min_y = min([y for side in surfaces for x, y, z in side]) - 1
max_y = max([y for side in surfaces for x, y, z in side]) + 1
min_z = min([z for side in surfaces for x, y, z in side]) - 1
max_z = max([z for side in surfaces for x, y, z in side]) + 1

start = (min_x, min_y, min_z)
queue = [start]
visited = set(start)
external_surfaces = set()

while len(queue) != 0:
    curr = queue[0]
    queue = queue[1:]

    x, y, z = curr[0], curr[1], curr[2]

    children = []
    if(x - 1 >= min_x):
        children.append((x-1, y, z))
        if(children[-1] in cube_coords):
            common_surface = get_common_surfaces(curr, children[-1])[0]
            external_surfaces.add(common_surface)

    if(x + 1 <= max_x):
        children.append((x+1, y, z))
        if(children[-1] in cube_coords):
            common_surface = get_common_surfaces(curr, children[-1])[0]
            external_surfaces.add(common_surface)

    if(y - 1 >= min_y):
        children.append((x, y-1, z))
        if(children[-1] in cube_coords):
            common_surface = get_common_surfaces(curr, children[-1])[0]
            external_surfaces.add(common_surface)
    if(y + 1 <= max_y):
        children.append((x, y+1, z))
        if(children[-1] in cube_coords):
            common_surface = get_common_surfaces(curr, children[-1])[0]
            external_surfaces.add(common_surface)

    if(z - 1 >= min_z):
        children.append((x, y, z-1))
        if(children[-1] in cube_coords):
            common_surface = get_common_surfaces(curr, children[-1])[0]
            external_surfaces.add(common_surface)
    if(z + 1 <= max_z):
        children.append((x, y, z+1))
        if(children[-1] in cube_coords):
            common_surface = get_common_surfaces(curr, children[-1])[0]
            external_surfaces.add(common_surface)

    queue.extend([child for child in children if child not in visited and child not in cube_coords])
    visited = visited.union(children)

print(len(external_surfaces))