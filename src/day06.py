
lines = []
with open("./data/day06.txt") as f:
    for line in f:
        if not line:
            continue
        lines.append(line)

last_signe = lines[4][0]
sous_total = 0
total = 0

for i in range(len(lines[0]) -1):

    if  i < len(lines[4]) and lines[4][i] != " ":
        last_signe = lines[4][i]
    
    if lines[0][i] == " " and lines[1][i] == " " and lines[2][i] == " " and lines[3][i] == " ":
        print(sous_total)
        total += sous_total
        sous_total = 0
        print("----")
        continue
        
    if last_signe == "+":
        sous_total += int("" + (lines[0][i] + lines[1][i] + lines[2][i] + lines[3][i]).replace(" ", ""))
        print("" + (lines[0][i] + lines[1][i] + lines[2][i] + lines[3][i]).replace(" ", "") + " +")
        
    elif last_signe == "*":
        if sous_total == 0:
            sous_total = 1
        sous_total *= int("" + (lines[0][i] + lines[1][i] + lines[2][i] + lines[3][i]).replace(" ", ""))
        print("" + (lines[0][i] + lines[1][i] + lines[2][i] + lines[3][i]).replace(" ", "") + " *")

total += sous_total
sous_total = 0
print("----")
        
print("Total =", total)