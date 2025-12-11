from itertools import product

machines = []
with open("./data/day10.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        machines.append(line)
        
# 1. Représenter chaque bouton comme un vecteur binaire
# 2. Représenter le pattern final comme un vecteur binaire
# 3. Résoudre A x = b en mod 2
# 4. Générer toutes les solutions via variables libres
# 5. Choisir la solution avec le moins de 1 → minimal presses

def split_machine_to_schema_and_boutons(line):
    parts = line.split(" ")
    schema_str = parts[0][1:-1] 
    schema = [1 if c == '#' else 0 for c in schema_str]

    boutons = []
    for part in parts[1:]:
        if part.startswith("(") and part.endswith(")"):
            bouton = tuple(map(int, part[1:-1].split(",")))
            bouton_vector = [0] * len(schema)
            for pos in bouton:
                bouton_vector[pos] = 1
            boutons.append(bouton_vector)

    return schema, boutons



def solve_machine(schema, boutons):
    """
    schema : liste de 0/1, taille m (nb de lumières)
    boutons : liste de vecteurs 0/1, chaque vecteur taille m (nb de lumières)
    Retourne : min nombre de pressions pour cette machine
    """
    m = len(schema)         # nb lignes (lumières)
    n = len(boutons)        # nb colonnes (boutons)

    if n == 0:
        # aucun bouton → soit déjà bon, soit impossible (AoC devrait pas mettre ça)
        return 0 if all(x == 0 for x in schema) else float('inf')

    # Construire la matrice A (m x n) : A[row][col]
    A = [[boutons[col][row] for col in range(n)] for row in range(m)]
    b = schema[:]

    # --- Gauss-Jordan mod 2 ---
    A = [row[:] for row in A]
    b = b[:]
    pivot_col_for_row = [-1] * m

    row = 0
    for col in range(n):
        # chercher pivot sur cette colonne
        sel = None
        for i in range(row, m):
            if A[i][col] == 1:
                sel = i
                break
        if sel is None:
            continue

        # swap lignes
        A[row], A[sel] = A[sel], A[row]
        b[row], b[sel] = b[sel], b[row]
        pivot_col_for_row[row] = col

        # éliminer sur toutes les autres lignes
        for i in range(m):
            if i != row and A[i][col] == 1:
                # ligne_i ^= ligne_row
                for j in range(col, n):
                    A[i][j] ^= A[row][j]
                b[i] ^= b[row]

        row += 1
        if row == m:
            break

    # Vérifier incohérence : 0...0 | 1
    for i in range(m):
        if all(x == 0 for x in A[i]) and b[i] == 1:
            return float('inf')  # pas de solution

    pivot_cols = [c for c in pivot_col_for_row if c != -1]
    free_cols = [c for c in range(n) if c not in pivot_cols]

    # Fonction pour reconstruire x à partir d'une assignation de free vars
    def build_solution(free_assign):
        x = [0] * n
        # poser les variables libres
        for idx, col in enumerate(free_cols):
            x[col] = free_assign[idx]

        # back-substitution sur les lignes pivot
        for i in range(m - 1, -1, -1):
            pc = pivot_col_for_row[i]
            if pc == -1:
                continue
            s = 0
            for j in range(pc + 1, n):
                if A[i][j] == 1 and x[j] == 1:
                    s ^= 1
            x[pc] = b[i] ^ s
        return x

    # Si aucune variable libre → solution unique
    if not free_cols:
        x = build_solution([])
        return sum(x)

    # Sinon, tester toutes les combinaisons des variables libres
    best = float('inf')
    for assign in product([0, 1], repeat=len(free_cols)):
        x = build_solution(assign)
        presses = sum(x)
        if presses < best:
            best = presses

    return best



print("*" * 40)
total = 0
for machine in machines:
    schema, boutons = split_machine_to_schema_and_boutons(machine)
    
    initial_state = '.' * (len(schema) -2)
    print(f"Schéma initiale : \t[{initial_state}]")
    print(f"Schema finale : \t{schema}")
    sous_total = solve_machine(schema, boutons)
    print("Nombre minimal de pressions pour cette machine :", sous_total)
    total += sous_total
    print("*" * 40)
    

print("Réponse partie 1 :", total)
