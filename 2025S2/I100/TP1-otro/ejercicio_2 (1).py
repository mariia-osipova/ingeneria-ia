from funciones_limpio import crear_grilla, simular_turno

N = 25
dc = 0.12
dz = 0.20
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

def main():
    edades_conejos_muertos = []
    edades_zorros_muertos = []
    for simulacion in range(100):
        grilla_actual = crear_grilla(N, dc, dz, dp, ec, ez)
        grilla_final, edades_z, edades_c = simular_turno(N, grilla_actual, turnos_totales, e_min, prz, prc, ez, ec, gc, gz, pp, edades_zorros_muertos, edades_conejos_muertos, animar=False)
    print(f'Muertes registradas - Conejos: {len(edades_conejos_muertos)} | Zorros: {len(edades_zorros_muertos)}')
    if len(edades_conejos_muertos) > 0:
        esperanza_conejo = sum(edades_conejos_muertos) / len(edades_conejos_muertos)
        print(f'Esperanza de vida del conejo: {esperanza_conejo:.2f} turnos')
    else:
        print('No hubo muertes de conejos registradas.')
    if len(edades_zorros_muertos) > 0:
        esperanza_zorro = sum(edades_zorros_muertos) / len(edades_zorros_muertos)
        print(f'Esperanza de vida del zorro: {esperanza_zorro:.2f} turnos')
    else:
        print('No hubo muertes de zorros registradas.')

if __name__ == "__main__":
    main()