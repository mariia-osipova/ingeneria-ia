import random

matrix_probability = [
    (0.6, 0.3, 0.05, 0.03, 0.02),
    (0.4, 0.3, 0.2, 0.05, 0.05),
    (0.1, 0.3, 0.4, 0.15, 0.05),
    (0.05, 0.1, 0.3, 0.5, 0.05),
    (0.05, 0.2, 0.2, 0.1, 0.45),
]

lista_status = ["soleado", "nublado", "lluvioso", "tormenta", "nevado"]

dicc_status = {
    "soleado": "☀️",
    "nublado": "☁️",
    "lluvioso": "🌧️",
    "tormenta": "⛈️",
    "nevado": "❄️",
}

status = input("estado inicial: ")
dias = int(input("dias: "))

def predict(status, dias):

    dias_soleado = 0
    dias_nublado = 0
    dias_lluvioso = 0
    dias_tormenta = 0
    dias_nevado = 0

    racha = 0

    racha_soleado = []
    racha_nublado = []
    racha_lluvioso = []
    racha_tormenta = []
    racha_nevado = []

    lista_dias_status = [status]

    for i in range(1, dias+1):

        lista_dias_status.append(status)

        if lista_dias_status[0] == lista_dias_status[1]:
            racha += 1
            if status == "soleado":
                racha_soleado.append(racha)
            elif status == "nublado":
                racha_nublado.append(racha)
            elif status == "lluvioso":
                racha_lluvioso.append(racha)
            elif status == "tormenta":
                racha_tormenta.append(racha)
            elif status == "nevado":
                racha_nevado.append(racha)
        else:
            racha = 0

        lista_dias_status.pop(0)

        if status == "soleado":
            dias_soleado += 1
        elif status == "nublado":
            dias_nublado += 1
        elif status == "lluvioso":
            dias_lluvioso += 1
        elif status == "tormenta":
            dias_tormenta += 1
        elif status == "nevado":
            dias_nevado += 1

        row_index = lista_status.index(status)
        status = random.choices(lista_status, weights=matrix_probability[row_index])[0]

        print(f"dia {i}: {dicc_status[status]} {status}")

        i += 1

    lista_racha = [racha_soleado, racha_nublado, racha_lluvioso, racha_tormenta, racha_nevado]
    k = 0

    for i in range(len(lista_racha)):
        for j in range(len(lista_racha[i])):
            if lista_racha[i][j] >= 3:
                k += 1
                j += 1
            else:
                j += 1
        i += 1

    max_racha_soleado = max(racha_soleado)
    max_racha_nublado = max(racha_nublado)
    max_racha_lluvioso = max(racha_lluvioso)
    max_racha_tormenta = max(racha_tormenta)
    max_racha_nevado = max(racha_nevado)

    lista_max_racha = [max_racha_soleado, max_racha_nublado, max_racha_lluvioso, max_racha_tormenta, max_racha_nevado]
    max_racha = max(lista_max_racha)
    max_racha_index = lista_max_racha.index(max_racha)
    clima_racha = lista_status[max_racha_index]

    print(f"racha de {max_racha} dias: {dicc_status[clima_racha]} {clima_racha} ")
    print(f"rachas de mas de 3 dias: {k}")

    frequency = [dias_soleado, dias_nublado, dias_lluvioso, dias_tormenta, dias_nevado]
    max_freq = max(frequency)
    max_freq_index = frequency.index(max_freq)

    s = "dias soleados:"
    n = "dias nublados:"
    l = "dias lluviosos:"
    t = "dias tormentas:"
    ne = "dias nevados:"

    len_s = len(s)
    len_n = len(n)
    len_l = len(l)
    len_t = len(t)
    len_ne = len(ne)

    length_max = max(len_s, len_n, len_l, len_t, len_ne) + 1

    dif_s = " " * (length_max - len_s)
    dif_n = " " * (length_max - len_n)
    dif_l = " " * (length_max - len_l)
    dif_t = " " * (length_max - len_t)
    dif_ne = " " * (length_max - len_ne)

    len_d_s = len(str(dias_soleado))
    len_d_n = len(str(dias_nublado))
    len_d_l = len(str(dias_lluvioso))
    len_d_t = len(str(dias_tormenta))
    len_d_ne = len(str(dias_nevado))

    length_max_dias = max(len_d_s, len_d_n, len_d_l, len_d_t, len_d_ne) + 1

    dif_d_s = " " * (length_max_dias - len_d_s)
    dif_d_n = " " * (length_max_dias - len_d_n)
    dif_d_l = " " * (length_max_dias - len_d_l)
    dif_d_t = " " * (length_max_dias - len_d_t)
    dif_d_ne = " " * (length_max_dias - len_d_ne)

    print(f"{s} {dif_s}{dias_soleado}{dif_d_s}({round(dias_soleado / dias * 100, 2)}%)")
    print(f"{n} {dif_n}{dias_nublado}{dif_d_n}({round(dias_nublado / dias * 100, 2)}%)")
    print(f"{l} {dif_l}{dias_lluvioso}{dif_d_l}({round(dias_lluvioso / dias * 100, 2)}%)")
    print(f"{t} {dif_t}{dias_tormenta}{dif_d_t}({round(dias_tormenta / dias * 100, 2)}%)")
    print(f"{ne} {dif_ne}{dias_nevado}{dif_d_ne}({round(dias_nevado / dias * 100, 2)}%)")

    print(f"el clima mas frequente: {dicc_status[lista_status[max_freq_index]]} {lista_status[max_freq_index]}")

predict(status, dias)