ranges = []
single_ids = []

with open("./data/day05.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        # Range
        if "-" in line:
            start, end = line.split("-")
            if start and end:
                ranges.append((int(start), int(end)))
        else:
            single_ids.append(int(line))

count = 0
for id_ in single_ids:
    for start, end in ranges:
        if start <= id_ <= end:
            count += 1
            break  
print("Count =", count)


ranges = []

with open("./data/day05.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        if "-" in line:
            start, end = map(int, line.split("-"))
            ranges.append((start, end))

ranges.sort()

merged = []
current_start, current_end = ranges[0]

for start, end in ranges[1:]:
    if start <= current_end + 1:
        current_end = max(current_end, end)
    else:
        merged.append((current_start, current_end))
        current_start, current_end = start, end

merged.append((current_start, current_end))

total = sum(end - start + 1 for start, end in merged)

print("Total fresh IDs:", total)
