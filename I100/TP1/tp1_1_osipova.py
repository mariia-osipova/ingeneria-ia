from I100.TP1.tp1_funciones_osipova import predict, clima_estable, count_rachas

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

status = input("ingrese estado inicial: ")

if status != str:
    while status not in lista_status:
        status = input("el estado inicial debe ser uno de: soleado, nublado, lluvioso, tormenta, nevado. ingrese el estado inicial: ")
    pass

dias = int(input("ingrese cantidad de dias: "))

if dias <= 0:
    while dias <= 0:
        dias = int(input("la cantidad de días debe ser un entero positivo. ingrese los dias: "))
    pass

# predict(status, dias, matrix_probability, lista_status, dicc_status)
# clima_estable(status, dias, matrix_probability, lista_status, dicc_status)
count_rachas(status, dias, matrix_probability, lista_status, dicc_status)