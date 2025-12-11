from itertools import product
from fractions import Fraction
import pulp


# ================================================================
#                           PARTIE 1
# ================================================================

def parse_machine_part1(line):
    parts = line.split()

    schema_str = parts[0][1:-1]
    schema = [1 if c == '#' else 0 for c in schema_str]
    n = len(schema)

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


def solve_machine_part1(schema, boutons):
    m = len(schema)
    n = len(boutons)

    # A[i][j] = effet du bouton j sur la lampe i
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

        # élimination gaussienne mod 2
        for i in range(m):
            if i != row and A[i][col] == 1:
                for j in range(col, n):
                    A[i][j] ^= A[row][j]
                b[i] ^= b[row]

        row += 1
        if row == m:
            break

    # système impossible ?
    for i in range(m):
        if all(A[i][j] == 0 for j in range(n)) and b[i] == 1:
            return float("inf")

    pivots = {pc for pc in pivot_col if pc != -1}
    free = [j for j in range(n) if j not in pivots]

    def build_x(assign):
        x = [0] * n
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
        return sum(build_x(()))

    best = float("inf")
    for assign in product([0, 1], repeat=len(free)):
        x = build_x(assign)
        best = min(best, sum(x))

    return best


# ================================================================
#                           PARTIE 2
# ================================================================

def parse_machine_part2(line):
    lb = line.index("{")
    rb = line.index("}")
    targets = list(map(int, line[lb + 1:rb].split(",")))

    parts = line[:lb].split()
    n = len(targets)
    boutons = []

    for p in parts:
        if p.startswith("(") and p.endswith(")"):
            inside = p[1:-1]
            idxs = list(map(int, inside.split(",")))
            vec = [0] * n
            for i in idxs:
                vec[i] = 1
            boutons.append(vec)

    return targets, boutons


def solve_machine_part2(targets, boutons):
    """
    Résout min sum(x_j)
    s.t.   sum_j boutons[j][i] * x_j = targets[i]   pour tout compteur i
           x_j entiers >= 0
    via pulp (ILP).
    """
    m = len(targets)
    n = len(boutons)

    # Si aucune cible non nulle, zéro appui suffit
    if all(t == 0 for t in targets):
        return 0

    # Création du problème ILP
    prob = pulp.LpProblem("AoC_Day10_Machine", pulp.LpMinimize)

    # Variables : x_j >= 0 entiers
    x = [pulp.LpVariable(f"x_{j}", lowBound=0, cat="Integer") for j in range(n)]

    # Objectif : minimiser le nombre total d'appuis
    prob += pulp.lpSum(x)

    # Contraintes : pour chaque compteur i
    for i in range(m):
        prob += pulp.lpSum(boutons[j][i] * x[j] for j in range(n)) == targets[i]

    # Résolution (CBC embarqué dans pulp, pas besoin d’install séparée)
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    if pulp.LpStatus[prob.status] != "Optimal":
        # En théorie AoC garantit solvable, donc ça ne devrait pas arriver
        # mais au pire on signale "inf"
        return float("inf")

    total_presses = 0
    for j in range(n):
        val = x[j].value()
        if val is None:
            return float("inf")
        total_presses += int(round(val))

    return total_presses


# ================================================================
#                           MAIN
# ================================================================

def main():
    machines = []
    with open("./data/day10.txt") as f:
        for line in f:
            line = line.strip()
            if line:
                machines.append(line)

    # PARTIE 1
    total1 = 0
    for line in machines:
        schema, boutons = parse_machine_part1(line)
        total1 += solve_machine_part1(schema, boutons)

    print("Réponse partie 1 :", total1)

    # PARTIE 2
    total2 = 0
    for line in machines:
        targets, boutons = parse_machine_part2(line)
        sous_total = solve_machine_part2(targets, boutons)
        print("  Sous-total :", sous_total)
        total2 += sous_total

    print("Réponse partie 2 :", total2)


if __name__ == "__main__":
    main()
