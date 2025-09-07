matrix_probability = [
    (0.6, 0.3, 0.05, 0.03, 0.02),
    (0.4, 0.3, 0.2, 0.05, 0.05),
    (0.1, 0.3, 0.4, 0.15, 0.05),
    (0.05, 0.1, 0.3, 0.5, 0.05),
    (0.05, 0.2, 0.2, 0.1, 0.45),
]

lista_status = ["soleado", "nubloso", "lluvioso", "tormenta", "nevado"]

status = input("status: ") in lista_status
dias = int(input("dias: "))

def predict(status, dias):

    if status == lista_status[0]:
        index = 0
    elif status == lista_status[1]:
        index = 1
    elif status == lista_status[2]:
        index = 2
    elif status == lista_status[3]:
        index = 3
    elif status == lista_status[4]:
        index = 4









