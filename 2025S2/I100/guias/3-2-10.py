
lista = [
    ( 20, 'Juan' ),
    ( 18, 'Pedro' ),
    ( 9, 'Esteban' )
]

print(
    f"+------+---------+\n"
    f"| Edad | Nombre |\n"
    f"+------+---------+"
)

for i in lista:
    print(
        f"| {i[0]} | {i[1]} |\n"
    )


ancho = len("+------+---------+")

def tablita(ancho, *text):
    print(1)
