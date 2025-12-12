import sys
from functools import lru_cache

# =====================
# Parsing
# =====================

with open("./data/day12.txt") as f:
    lines = [l.rstrip() for l in f if l.strip()]

forms = []
regions = []

i = 0
while i < len(lines) and lines[i].endswith(":") and lines[i][:-1].isdigit():
    i += 1
    shape = []
    while i < len(lines) and set(lines[i]) <= {"#", "."}:
        shape.append(lines[i])
        i += 1
    forms.append(shape)

for l in lines[i:]:
    size, rest = l.split(":")
    w, h = map(int, size.split("x"))
    counts = list(map(int, rest.split()))
    regions.append((w, h, counts))

# =====================
# Shapes transforms
# =====================

def rotations(shape):
    res = set()
    h, w = len(shape), len(shape[0])
    grid = tuple(tuple(c for c in row) for row in shape)

    def rot(g):
        return tuple(zip(*g[::-1]))

    def flip(g):
        return tuple(row[::-1] for row in g)

    g = grid
    for _ in range(4):
        for v in (g, flip(g)):
            coords = tuple(
                (i, j)
                for i in range(len(v))
                for j in range(len(v[0]))
                if v[i][j] == "#"
            )
            minx = min(x for x, _ in coords)
            miny = min(y for _, y in coords)
            norm = tuple(sorted((x - minx, y - miny) for x, y in coords))
            res.add(norm)
        g = rot(g)
    return list(res)

FORMES = [rotations(f) for f in forms]
AREAS = [len(f[0]) for f in FORMES]

# =====================
# Solver
# =====================

def solve_region(w, h, counts):
    total_area = sum(counts[i] * AREAS[i] for i in range(6))
    if total_area > w * h:
        return False

    pieces = []
    for i in range(6):
        for _ in range(counts[i]):
            pieces.append(i)

    # ordre: formes les + grosses d'abord
    pieces.sort(key=lambda i: -AREAS[i])

    placements = []
    piece_ids = []

    for pid, p in enumerate(pieces):
        for shape in FORMES[p]:
            maxx = max(x for x, _ in shape)
            maxy = max(y for _, y in shape)
            for x in range(h - maxx):
                for y in range(w - maxy):
                    mask = 0
                    ok = True
                    for dx, dy in shape:
                        cx = x + dx
                        cy = y + dy
                        bit = cx * w + cy
                        mask |= 1 << bit
                    placements.append(mask)
                    piece_ids.append(pid)

    N = len(pieces)

    used_piece = [False] * N
    used_mask = 0

    by_piece = [[] for _ in range(N)]
    for i, pid in enumerate(piece_ids):
        by_piece[pid].append(i)

    sys.setrecursionlimit(10000)

    def dfs(k):
        nonlocal used_mask
        if k == N:
            return True

        # pick next unused piece
        while k < N and used_piece[k]:
            k += 1
        if k == N:
            return True

        for idx in by_piece[k]:
            m = placements[idx]
            if m & used_mask:
                continue
            used_piece[k] = True
            prev = used_mask
            used_mask |= m
            if dfs(k + 1):
                return True
            used_mask = prev
            used_piece[k] = False
        return False

    return dfs(0)

# =====================
# Run all regions
# =====================

from concurrent.futures import ProcessPoolExecutor
import os
sys.setrecursionlimit(200000)


def solve_one(region):
    w, h, counts = region
    ok = solve_region(w, h, counts)
    return ok, w, h, counts

if __name__ == "__main__":
    ans = 0
    MAX_WORKERS = 6

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as pool:

        for ok, w, h, counts in pool.map(solve_one, regions):
            if ok:
                ans += 1
            print(f"Region {w}x{h} with counts {counts} is {'solvable' if ok else 'not solvable'}")

    print(ans)
# 40 39 38 41 37 30