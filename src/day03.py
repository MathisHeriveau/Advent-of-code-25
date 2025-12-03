with open("./data/day03.txt") as f:
    somme = 0
    fenetre = 12
    for line in f:
        digits = list(line.strip())

        result = ""
        n = len(digits)

        start = 0
        for _ in range(fenetre):
            end = n - (fenetre - len(result)) + 1

            window = digits[start:end]
            print(window)
            max_value = max(window)
            max_index = window.index(max_value) + start

            result += max_value

            start = max_index + 1

        somme += int(result)

    print(somme)
