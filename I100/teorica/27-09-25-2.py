def whoisthewinner():
    score = [0, 0]
    s = input().strip()
    print(*score)

    while True:
        try:
            s = input().strip()
        except EOFError:
            break
        if s == "":
            break
        if s not in ("1", "2"):
            while s not in ("1", "2"):
                try:
                    s = input().strip()
                except EOFError:
                    break
                if s == "":
                    break

        i = 0 if s == "1" else 1
        j = 1 - i

        if score[i] in (0, 15):
            score[i] += 15
            print(*score)
        elif score[i] == 30:
            score[i] = 40
            print(*score)
        elif score[i] == 40 and score[j] in (0, 15, 30):
            print(f"Gana el jugador {i+1}")
            return
        elif score[i] == 40 and score[j] == 40:
            score[i] = "Adv"
            print(*score)
        elif score[i] == "Adv" and score[j] == 40:
            print(f"Gana el jugador {i+1}")
            return
        elif score[i] == 40 and score[j] == "Adv":
            score[j] = 40
            print(*score)

whoisthewinner()