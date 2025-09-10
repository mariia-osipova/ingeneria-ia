import random

matrix_probability = [
    (0.6, 0.3, 0.05, 0.03, 0.02),
    (0.4, 0.3, 0.2, 0.05, 0.05),
    (0.1, 0.3, 0.4, 0.15, 0.05),
    (0.05, 0.1, 0.3, 0.5, 0.05),
    (0.05, 0.2, 0.2, 0.1, 0.45),
]

lista_status = ["soleado", "nubloso", "lluvioso", "tormenta", "nevado"]

status = input("estado inicial: ")
dias = int(input("dias: "))

def predict(status, dias):

    dias_soleado = 0
    dias_nubloso = 0
    dias_lluvioso = 0
    dias_tormenta = 0
    dias_nevado = 0

    for i in range(1, dias+1):

        if status == "soleado":
            dias_soleado += 1
        elif status == "nubloso":
            dias_nubloso += 1
        elif status == "lluvioso":
            dias_lluvioso += 1
        elif status == "tormenta":
            dias_tormenta += 1
        elif status == "nevado":
            dias_nevado += 1

        row_index = lista_status.index(status)
        status = random.choices(lista_status, weights=matrix_probability[row_index])[0]

        print(f"dia {i}: {status}")
        i += 1

    frequency = [dias_soleado, dias_nubloso, dias_lluvioso, dias_tormenta, dias_nevado]

    max_freq = max(frequency)

    max_freq_index = frequency.index(max_freq)

    length_s = len("dias soleados:")
    length_n = len("dias nubloso:")
    length_l = len("dias lluvioso:")
    length_t = len("dias tormenta:")
    length_ne = len("dias nevado:")

    print(length_s, length_n, length_l, length_t, length_ne)

    length_max = max(length_s, length_n, length_l, length_t, length_ne) + 1

    dif_s = " " * (length_max - length_s)
    dif_n = (length_max - length_n) * " "
    dif_l = (length_max - length_l) * " "
    dif_t = (length_max - length_t) * " "
    dif_ne = (length_max - length_ne) * " "

    print(f"dias soleados:{dif_s}{dias_soleado} ({round(dias_soleado / dias * 100, 2)}%)")
    print(f"dias nublosos:{dif_n}{dias_nubloso} ({round(dias_nubloso / dias * 100, 2)}%)")
    print(f"dias lluviosos:{dif_l}{dias_lluvioso} ({round(dias_lluvioso / dias * 100, 2)}%)")
    print(f"dias tormenta:{dif_t}{dias_tormenta} ({round(dias_tormenta / dias * 100, 2)}%)")
    print(f"dias nevados:{dif_ne}{dias_nevado} ({round(dias_nevado / dias * 100, 2)}%)")

    print(f"clima mas frequente: {lista_status[max_freq_index]}")

predict(status, dias)


