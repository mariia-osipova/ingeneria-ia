h_trabajo = float(input())
precio_h = float(input())

if h_trabajo <= 35:
    sueldo = h_trabajo * precio_h
else:
    sueldo = ((h_trabajo - 35) * precio_h * 1.5) + (35 * precio_h)

if sueldo < 500:
    sueldo = sueldo
else:
    if sueldo >= 900:
        imp1 = (sueldo - 500) * 0.25
        imp2 = (sueldo - 900) * 0.45
    else:
        imp1 = (sueldo - 500) * 0.25
        imp2 = 0

    sueldo = sueldo - imp1 - imp2

print(sueldo)

print(sueldo)
