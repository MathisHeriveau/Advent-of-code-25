import math
from itertools import combinations

# -------------------------
#   Lecture du fichier
# -------------------------
points = []
with open("./data/day08.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        x, y, z = map(int, line.split(","))
        points.append((x, y, z))

n = len(points)
print("Nombre de points :", n)

# -------------------------
#   Union-Find
# -------------------------
parent = list(range(n))
size = [1] * n
components = n

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(a, b):
    global components
    ra, rb = find(a), find(b)
    if ra == rb:
        return False
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    size[ra] += size[rb]
    components -= 1
    return True

# -------------------------
#   Calcul des distances (sans racine → plus rapide)
# -------------------------
distances = []
for i in range(n):
    x1, y1, z1 = points[i]
    for j in range(i+1, n):
        x2, y2, z2 = points[j]
        d = (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2
        distances.append((d, i, j))

print("Nombre de paires :", len(distances))

# Trie global de toutes les distances
distances.sort(key=lambda t: t[0])

# -------------------------
#   On connecte jusqu’à avoir 1 seul circuit
# -------------------------
last_pair = None

for _, i, j in distances:
    if union(i, j):
        last_pair = (i, j)
        if components == 1:
            break

# -------------------------
#   Résultat Partie 2
# -------------------------
a, b = last_pair
x1, _, _ = points[a]
x2, _, _ = points[b]

print("Dernière paire connectée :", points[a], points[b])
print("Réponse Partie 2 =", x1 * x2)
