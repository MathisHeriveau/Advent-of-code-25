point = 50
zero = 0

with open("./data/day01.txt") as f:
    for line in f:
        line = line.strip()
        d = line[0]
        dist = int(line[1:])

        for _ in range(dist):
            if d == "R":
                point = (point + 1) % 100
            else:
                point = (point - 1) % 100

            if point == 0:
                zero += 1

print(point)
print(zero)
