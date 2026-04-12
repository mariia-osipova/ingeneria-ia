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

edades_conejos_muertos = []
edades_zorros_muertos = []

def main():
    grilla_actual = crear_grilla(N, dc, dz, dp, ec, ez)
    grilla_final, edades_z, edades_c = simular_turno(N, grilla_actual, turnos_totales, e_min, prz, prc, ez, ec, gc, gz, pp, edades_zorros_muertos, edades_conejos_muertos)
    
if __name__ == "__main__":
    main()