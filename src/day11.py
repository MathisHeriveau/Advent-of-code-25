from collections import defaultdict
from functools import lru_cache

# ================== PARSING COMMUN ==================

def parse_input(lines):
    graph = defaultdict(list)
    for line in lines:
        line = line.strip()
        if not line:
            continue
        left, right = line.split(":")
        src = left.strip()
        dests = right.strip().split()
        graph[src].extend(dests)
    return graph


def build_graph_from_file(path):
    with open(path) as f:
        lines = f.readlines()
    return parse_input(lines)

# ================== PARTIE 1 ==================

def count_paths_simple(graph, start="you", end="out"):
    @lru_cache(maxsize=None)
    def dfs(node):
        if node == end:
            return 1
        if node not in graph or not graph[node]:
            return 0
        total = 0
        for nxt in graph[node]:
            total += dfs(nxt)
        return total

    return dfs(start)

# ================== PARTIE 2 ==================

def count_paths_with_required(graph, start="svr", end="out",
                              must1="dac", must2="fft"):
    @lru_cache(maxsize=None)
    def dfs(node, mask):
        if node == must1:
            mask |= 1
        if node == must2:
            mask |= 2 

        if node == end:
            return 1 if mask == 3 else 0

        if node not in graph or not graph[node]:
            return 0

        total = 0
        for nxt in graph[node]:
            total += dfs(nxt, mask)
        return total

    return dfs(start, 0)

# ================== MAIN ==================

def main():
    graph = build_graph_from_file("./data/day11.txt")

    res1 = count_paths_simple(graph, "you", "out")
    print("Réponse partie 1 :", res1)

    res2 = count_paths_with_required(graph, "svr", "out", "dac", "fft")
    print("Réponse partie 2 :", res2)


if __name__ == "__main__":
    main()
