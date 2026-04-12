from funciones_limpio import crear_grilla, simular_turno, contar_animales

N = 25
dc = 0.12
dp = 0.35
ec = 5
ez = 12
gc = 4
gz = 8
pp = 0.50
prc = 0.18
prz = 0.18
e_min = 4
turnos_totales = 200

edades_conejos_muertos = [] # En este ejercicio las edades no importan, pero la función simular_turno las pide
edades_zorros_muertos = []

def main():
    print('+--------+---------------------+')
    print('|  d_z   |   Sin extinciones   |')
    print('+--------+---------------------+')
    valores_dz = [i / 100 for i in range(1, 40, 2)]
    for dz in valores_dz:
        exitos = 0
        for simulacion in range(50):
            grilla_actual = crear_grilla(N, dc, dz, dp, ec, ez)
            grilla_final, edades_z, edades_c = simular_turno(N, grilla_actual, turnos_totales, e_min, prz, prc, ez, ec, gc, gz, pp, edades_zorros_muertos, edades_conejos_muertos, animar=False)
            conejos_finales, zorros_finales = contar_animales(grilla_final, N)
            if conejos_finales > 0 and zorros_finales > 0:
                exitos += 1
        porcentaje = (exitos / 50) * 100
        print(f'| {dz:<6.2f} | {porcentaje:>7.2f} %           |')
        print('+--------+---------------------+')

if __name__ == "__main__":
    main()