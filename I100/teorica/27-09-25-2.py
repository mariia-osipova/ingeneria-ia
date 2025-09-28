def whoisthewinner():
    score = [0, 0]

    while True:
        s = input().strip()
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
            print(*score)
            score[i] += 15
        elif score[i] == 30:
            print(*score)
            score[i] = 40
        elif score[i] == 40 and score[j] in (0, 15, 30):
            print(*score)
            print(f"Gana el jugador {i+1}")
            return
        elif score[i] == 40 and score[j] == 40:
            print(*score)
            score[i] = "Adv"
        elif score[i] == "Adv" and score[j] == 40:
            print(*score)
            print(f"Gana el jugador {i+1}")
            return
        elif score[i] == 40 and score[j] == "Adv":
            print(*score)
            score[j] = 40

whoisthewinner()