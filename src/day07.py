lines = []
with open("./data/day07.txt") as f:
    for line in f:
        if not line:
            continue
        lines.append(line.rstrip("\n")) 


lines = [list(line) for line in lines]
count = 0
for i, line in enumerate(lines):
    for j, char in enumerate(line):
        if i == len(lines) - 1:
            continue
        if char == "S":
            lines[i+1][j] = "|"
        
        if char == "|": 
            if lines[i+1][j] != "^":
                lines[i+1][j] = "|"
            else:
                lines[i+1][j+1] = "|"
                lines[i+1][j-1] = "|"
                count += 1

lines = ["".join(line) for line in lines]

for line in lines:
    print(line)

print("Total =", count)

H = len(lines)
W = len(lines[0])

dp = [[0]*W for _ in range(H)]

for j, c in enumerate(lines[0]):
    if c == "S":
        dp[0][j] = 1
        
for i in range(H-1):
    for j in range(W):
        cur = dp[i][j]
        if cur == 0:
            continue

        cell = lines[i][j]

        if cell in (".", "S", "|"):
            dp[i+1][j] += cur

        if cell == "^":
            if j > 0:
                dp[i+1][j-1] += cur
            if j < W-1:
                dp[i+1][j+1] += cur

answer = sum(dp[H-1])


print("Total =", answer)
