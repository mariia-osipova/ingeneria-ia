import random

def predict(status, dias, matrix_probability, lista_status, dicc_status):
    """
    predict the next day's state using a Markov transition matrix.

    args:
        status: el clima del dia actual que se va actualizando
        dias: la cantidad de dias que quiero describir
        matrix_probability: a Markov matrix
        lista_status: todas mis climas que se pueden ocurrir
        dicc_status: emojis para mis climas

    returns:
        none. prints the result for each day.
    """

    for i in range(1, dias + 1):
        print(f"dia {i}: {dicc_status[status]} {status}")
        row_index = lista_status.index(status)
        status = random.choices(lista_status, weights=matrix_probability[row_index])[0]

def clima_estable(status, dias, matrix_probability, lista_status, dicc_status):
    """
    computes the longest streak of consecutive identical weather states

    args:
        status: el clima del dia actual que se va actualizando
        dias: la cantidad de dias que quiero describir
        matrix_probability: a Markov matrix
        lista_status: todas mis climas que se pueden ocurrir
        dicc_status: emojis para mis climas

    returns:
        none. prints the longest streak
    """
    dias_soleado = 0
    dias_nublado = 0
    dias_lluvioso = 0
    dias_tormenta = 0
    dias_nevado = 0

    for i in range(1, dias + 1):

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

    frequency = [dias_soleado, dias_nublado, dias_lluvioso, dias_tormenta, dias_nevado]
    max_freq = max(frequency)
    max_freq_index = frequency.index(max_freq)

    print_clima_estable(dias_soleado, dias_nublado, dias_lluvioso, dias_tormenta, dias_nevado, max_freq_index, lista_status, dicc_status, dias)

def count_rachas(status, dias, matrix_probability, lista_status, dicc_status):

    """
    computes the quantity of streaks lasting more that 3 days

    args:
        status: el clima del dia actual que se va actualizando
        dias: la cantidad de dias que quiero describir
        matrix_probability: a Markov matrix
        lista_status: todas mis climas que se pueden ocurrir
        dicc_status: emojis para mis climas

    returns:
        none. prints the quantity of streaks lasting more that 3 days

    """

    racha_soleado = []
    racha_nublado =  []
    racha_lluvioso = []
    racha_tormenta = []
    racha_nevado = []

    previous_status = None
    racha = 0

    for i in range(1, dias + 1):
        if previous_status is None:
            previous_status = status
            racha = 1
        elif status == previous_status:
            racha += 1
        else:
            if previous_status == "soleado":
                racha_soleado.append(racha)
            elif previous_status == "nublado":
                racha_nublado.append(racha)
            elif previous_status == "lluvioso":
                racha_lluvioso.append(racha)
            elif previous_status == "tormenta":
                racha_tormenta.append(racha)
            elif previous_status == "nevado":
                racha_nevado.append(racha)

            previous_status = status
            racha = 1

        row_index = lista_status.index(status)
        status = random.choices(lista_status, weights=matrix_probability[row_index])[0]

    if previous_status == "soleado":
        racha_soleado.append(racha)
    elif previous_status == "nublado":
        racha_nublado.append(racha)
    elif previous_status == "lluvioso":
        racha_lluvioso.append(racha)
    elif previous_status == "tormenta":
        racha_tormenta.append(racha)
    elif previous_status == "nevado":
        racha_nevado.append(racha)

    k = (sum(x > 3 for x in racha_soleado) +
         sum(x > 3 for x in racha_nublado) +
         sum(x > 3 for x in racha_lluvioso) +
         sum(x > 3 for x in racha_tormenta) +
         sum(x > 3 for x in racha_nevado)
    )

    lista_max_racha = [
        max(racha_soleado or [0]), max(racha_nublado or [0]), max(racha_lluvioso or [0]), max(racha_tormenta or [0]), max(racha_nevado or [0])
    ]

    max_racha = max(lista_max_racha or [0])

    max_racha_index = lista_max_racha.index(max_racha)
    clima_racha = lista_status[max_racha_index]

    print_racha(max_racha, dicc_status, clima_racha, k)

def print_clima_estable(dias_soleado, dias_nublado, dias_lluvioso, dias_tormenta, dias_nevado, max_freq_index, lista_status, dicc_status, dias):
    """
    prints the result of the function clima_estable()
    """

    s = "dias soleados:"
    n = "dias nublados:"
    l = "dias lluviosos:"
    t = "dias tormentas:"
    ne = "dias nevados:"

    length_max = max(len(s), len(n), len(l), len(t), len(ne)) + 1

    dif_s = " " * (length_max - len(s))
    dif_n = " " * (length_max - len(n))
    dif_l = " " * (length_max - len(l))
    dif_t = " " * (length_max - len(t))
    dif_ne = " " * (length_max - len(ne))

    length_max_dias = max(len(str(dias_soleado)), len(str(dias_nublado)), len(str(dias_lluvioso)),
                          len(str(dias_tormenta)), len(str(dias_nevado))) + 1

    dif_d_s = " " * (length_max_dias - len(str(dias_soleado)))
    dif_d_n = " " * (length_max_dias - len(str(dias_nublado)))
    dif_d_l = " " * (length_max_dias - len(str(dias_lluvioso)))
    dif_d_t = " " * (length_max_dias - len(str(dias_tormenta)))
    dif_d_ne = " " * (length_max_dias - len(str(dias_nevado)))

    print(f"\n{s} {dif_s}{dias_soleado}{dif_d_s}({round(dias_soleado / dias * 100, 2)}%)")
    print(f"{n} {dif_n}{dias_nublado}{dif_d_n}({round(dias_nublado / dias * 100, 2)}%)")
    print(f"{l} {dif_l}{dias_lluvioso}{dif_d_l}({round(dias_lluvioso / dias * 100, 2)}%)")
    print(f"{t} {dif_t}{dias_tormenta}{dif_d_t}({round(dias_tormenta / dias * 100, 2)}%)")
    print(f"{ne} {dif_ne}{dias_nevado}{dif_d_ne}({round(dias_nevado / dias * 100, 2)}%)")

    print(f"\nel clima mas frequente: {dicc_status[lista_status[max_freq_index]]} {lista_status[max_freq_index]}")

def print_racha(max_racha, dicc_status, clima_racha, k):
    """
    prints the result of the function count_rachas()
    """

    print(f"racha de {max_racha} dias: {dicc_status[clima_racha]} {clima_racha} ")
    print(f"rachas de mas de 3 dias: {k}")