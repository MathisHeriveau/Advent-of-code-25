from itertools import product
from fractions import Fraction

# ========================================
# ============  PARSING PART 1  ==========
# ========================================

def parse_machine_part1(line):
    parts = line.split()

    # 1. Schéma entre [ ]
    schema_str = parts[0][1:-1]
    schema = [1 if c == '#' else 0 for c in schema_str]
    n = len(schema)

    # 2. Boutons
    boutons = []
    for p in parts[1:]:
        if p.startswith("(") and p.endswith(")"):
            inside = p[1:-1]
            idxs = list(map(int, inside.split(",")))
            vec = [0] * n
            for i in idxs:
                vec[i] = 1
            boutons.append(vec)

    return schema, boutons


# ========================================
# ========  PART 1 SOLVEUR MOD 2 =========
# ========================================

def solve_machine_part1(schema, boutons):
    m = len(schema)
    n = len(boutons)

    A = [[boutons[j][i] for j in range(n)] for i in range(m)]
    b = schema[:]

    A = [row[:] for row in A]
    b = b[:]
    pivot_col = [-1] * m

    row = 0
    for col in range(n):
        sel = None
        for i in range(row, m):
            if A[i][col] == 1:
                sel = i
                break
        if sel is None:
            continue

        A[row], A[sel] = A[sel], A[row]
        b[row], b[sel] = b[sel], b[row]
        pivot_col[row] = col

        for i in range(m):
            if i != row and A[i][col] == 1:
                for j in range(col, n):
                    A[i][j] ^= A[row][j]
                b[i] ^= b[row]

        row += 1
        if row == m:
            break

    # Check inconsistent
    for i in range(m):
        if all(A[i][j] == 0 for j in range(n)) and b[i] == 1:
            return float("inf")

    pivots = {pc for pc in pivot_col if pc != -1}
    free = [j for j in range(n) if j not in pivots]

    def build_x(assign):
        x = [0]*n
        for idx, col in enumerate(free):
            x[col] = assign[idx]

        for i in reversed(range(m)):
            pc = pivot_col[i]
            if pc == -1:
                continue
            s = 0
            for j in range(pc+1, n):
                if A[i][j] == 1 and x[j] == 1:
                    s ^= 1
            x[pc] = b[i] ^ s
        return x

    if not free:
        return sum(build_x([]))

    best = float("inf")
    for assign in product([0,1], repeat=len(free)):
        x = build_x(assign)
        best = min(best, sum(x))

    return best


# ========================================
# ============  PARSING PART 2  ==========
# ========================================

def parse_machine_part2(line):
    lb = line.index("{")
    rb = line.index("}")
    targets = list(map(int, line[lb+1:rb].split(",")))

    before = line[:lb]
    parts = before.split()

    n = len(targets)
    boutons = []

    for p in parts:
        if p.startswith("(") and p.endswith(")"):
            inside = p[1:-1]
            idxs = list(map(int, inside.split(",")))
            vec = [0]*n
            for i in idxs:
                vec[i] = 1
            boutons.append(vec)

    return targets, boutons


# ========================================
# =========  PART 2 ILP SOLVEUR  =========
# ========================================

def solve_machine_part2(targets, boutons):
    m = len(targets)
    n = len(boutons)

    A = [[Fraction(boutons[j][i]) for j in range(n)] for i in range(m)]
    b = [Fraction(t) for t in targets]

    pivot_col = [-1]*m
    row = 0

    # --- Gauss rationnel ---
    for col in range(n):
        sel = None
        for i in range(row, m):
            if A[i][col] != 0:
                sel = i
                break
        if sel is None:
            continue

        A[row], A[sel] = A[sel], A[row]
        b[row], b[sel] = b[sel], b[row]
        pivot = A[row][col]

        inv = Fraction(1,1) / pivot
        for j in range(col, n):
            A[row][j] *= inv
        b[row] *= inv

        pivot_col[row] = col

        for i in range(m):
            if i != row and A[i][col] != 0:
                f = A[i][col]
                for j in range(col, n):
                    A[i][j] -= f*A[row][j]
                b[i] -= f*b[row]

        row += 1
        if row == m:
            break

    # Impossible ?
    for i in range(m):
        if all(A[i][j] == 0 for j in range(n)) and b[i] != 0:
            return float("inf")

    pivots = {pc for pc in pivot_col if pc != -1}
    free = [j for j in range(n) if j not in pivots]

    def build_x(params):
        x = [Fraction(0)]*n
        for col,val in params.items():
            x[col] = Fraction(val)

        for i in reversed(range(m)):
            pc = pivot_col[i]
            if pc == -1:
                continue
            s = 0
            for j in range(pc+1, n):
                s += A[i][j]*x[j]
            x[pc] = b[i] - s

        return x

    if not free:
        x = build_x({})
        if any(xx < 0 or xx.denominator != 1 for xx in x):
            return float("inf")
        return sum(int(xx) for xx in x)

    bound = max(targets)
    best = float("inf")

    if len(free) == 1:
        f = free[0]
        for t in range(bound+1):
            x = build_x({f:t})
            ok = True
            tot = 0
            for xx in x:
                if xx < 0 or xx.denominator != 1:
                    ok = False
                    break
                tot += int(xx)
            if ok and tot < best:
                best = tot
        return best

    if len(free) == 2:
        f1,f2 = free
        for t1 in range(bound+1):
            for t2 in range(bound+1):
                x = build_x({f1:t1, f2:t2})
                ok = True
                tot = 0
                for xx in x:
                    if xx < 0 or xx.denominator != 1:
                        ok = False
                        break
                    tot += int(xx)
                if ok and tot < best:
                    best = tot
        return best

    return best


# ========================================
# ===============  MAIN  =================
# ========================================

machines = []
with open("./data/day10.txt") as f:
    for line in f:
        line=line.strip()
        if line:
            machines.append(line)

# PART 1
total1 = 0
for line in machines:
    schema, boutons = parse_machine_part1(line)
    total1 += solve_machine_part1(schema, boutons)

print("Réponse partie 1 :", total1)

# PART 2
total2 = 0
for line in machines:
    targets, boutons = parse_machine_part2(line)
    total2 += solve_machine_part2(targets, boutons)

print("Réponse partie 2 :", total2)
