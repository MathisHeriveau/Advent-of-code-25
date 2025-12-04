tab = []
new_tab = []
counter = 0
total = 0

with open("./data/day04.txt") as f:
    for line in f:
        tab.append(list(line.strip()))
        
new_tab = [row.copy() for row in tab]

def verify(row, char):
    if tab[row][char] != "@":
        return False

    around = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue 
            
            nr, nc = row + x, char + y
            if 0 <= nr < len(tab) and 0 <= nc < len(tab[row]):
                if tab[nr][nc] == "@":
                    around += 1

    if around >= 4:
        return False
    
    new_tab[row][char] = "#"
    
    return True


for i in range(len(tab)):
    for j in range(len(tab[i])):
        if verify(i, j):
            counter += 1

for l in new_tab:
    print("".join(l))
    
run = 1
total += counter

while counter != -1:
    counter = 0
    for i in range(len(new_tab)):
        for j in range(len(new_tab[i])):
            if new_tab[i][j] == "#":
                new_tab[i][j] = "."
                
    tab = [row.copy() for row in new_tab]
    
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            if verify(i, j):
                counter += 1

    for l in new_tab:
        print("".join(l))
        
    if (counter == 0):
        counter = -1
    else :
        run += 1
        total += counter

print("Runs:", run)
print("Total infected:", total)