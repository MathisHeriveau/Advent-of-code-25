def is_invalid_id(n: int) -> bool:
    s = str(n)
    if len(s) % 2 != 0:
        return False
    mid = len(s) // 2
    return s[:mid] == s[mid:] 


def solve(puzzle_line: str) -> int:
    total = 0
    ranges = puzzle_line.strip().split(",")

    for r in ranges:
        if not r:
            continue
        start, end = map(int, r.split("-"))
        for n in range(start, end + 1):
            if is_invalid_id(n):
                total += n

    return total

def is_invalid_id_part2(n: int) -> bool:
    s = str(n)
    L = len(s)

    for motif_len in range(1, L // 2 + 1):
        if L % motif_len != 0:
            continue 

        repeat_count = L // motif_len
        if repeat_count < 2:
            continue  

        motif = s[:motif_len]
        if motif * repeat_count == s:
            return True

    return False


def solve_part2(puzzle_line: str) -> int:
    total = 0
    ranges = puzzle_line.strip().split(",")

    for r in ranges:
        if not r:
            continue
        start, end = map(int, r.split("-"))
        for n in range(start, end + 1):
            if is_invalid_id_part2(n):
                total += n

    return total


with open("./data/day02.txt") as f:
    example = f.read()
    result = solve_part2(example)
    print(result)  
    

