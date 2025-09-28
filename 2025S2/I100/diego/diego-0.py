import numpy as np

def diego():
    costo_total = 0
    oferta = [100, 150, 75]
    demanda = [50, 125, 150]
    costos = np.array([
                    [5,8,3],
                    [4,7,6],
                    [9,2,5]
    ])

    if sum(oferta) != sum(demanda):
        print("tarado, this does not work")
        return
    else:
        print("ok puede ser... processando la solucion")

        while sum(oferta) > 0 and sum(demanda) > 0:
            min_value = min(val for row in costos for val in row if val != 0)
            row, col = np.where(costos == min_value) #JAJAJAJAJA wtf for me there is a better way to find the index of the min but anyway
            i = row[0]
            j = col[0]

            if oferta[i] < demanda[j]:
                pago = oferta[i]
            else:
                pago = demanda[j]

            oferta[i] -= pago
            demanda[j] -= pago
            costo_total += min_value * pago

            costos[i][j] = 0

        return(int(costo_total))

print(diego())
