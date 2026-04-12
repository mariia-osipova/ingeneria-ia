# TP1 — Reporte de Errores y Mejoras (verificado contra el enunciado)

---

## Error 1 — CRASH: `contar_animales` llamada sin el argumento `N`

**Archivo:** `ejercicio_3.py`, línea 29
**Severidad:** CRÍTICO — el programa crashea siempre

### Qué dice el código
```python
conejos_finales, zorros_finales = contar_animales(grilla_final)
```

### Por qué no funciona
La función en `funciones_limpio.py` tiene la firma:
```python
def contar_animales(snapshot, N):
```
Requiere dos argumentos. La llamada pasa uno → `TypeError` inmediato en cada iteración.

### Qué exige el enunciado
El ejercicio 3 pide variar `dz` de 0.01 a 0.39 en incrementos de 0.02, correr 50 simulaciones por valor, y reportar el porcentaje de coexistencia. Al crashear antes del conteo, el programa **nunca produce output alguno**.

### Cómo corregirlo
```python
conejos_finales, zorros_finales = contar_animales(grilla_final, N)
```

---

## Error 2 — CÓDIGO MUERTO + INCUMPLIMIENTO DE SPEC: Lógica de alimentación en el paso incorrecto

**Archivo:** `funciones_limpio.py`, línea 143
**Severidad:** ALTO — código muerto que además viola la spec; genera muertes no registradas

### Qué dice el código
```python
# Dentro de mover_y_reproducir_zorros (Paso 3 — movimiento de zorros)
if type(snapshot[x][y]) is dict and snapshot[x][y] == 'conejo':
    zorro['energia'] += gz
```

### Problema 1: El código nunca se ejecuta (dead code)
La condición compara un **diccionario** con el string `'conejo'`. Un diccionario nunca puede ser igual a un string → condición siempre `False` → `zorro['energia'] += gz` nunca corre.

### Problema 2: Está en el paso equivocado según el enunciado
El enunciado dice explícitamente:

> **Paso 4 — Movimiento de los conejos:** "Si su celda destino tiene un zorro (en la nueva grilla): el zorro come al conejo, gana gz puntos de energía, y se registra la edad del conejo."

La transferencia de energía ocurre en el **Paso 4 (movimiento de conejos)**, no en el Paso 3 (movimiento de zorros). Esta línea intenta hacerlo en el paso equivocado.

### ¿Los zorros ganan energía entonces?
Sí — correctamente, a través de `mover_y_reproducir_conejos`:
```python
if es_zorro:
    nueva[x][y]['energia'] += gz   # ← esto sí se ejecuta y está bien
    edades_conejos_muertos.append(conejo['edad'])
```
Esto respeta el Paso 4 del enunciado. ✓

### Problema 3: Conejos que mueren en el Paso 3 no se registran
Cuando un zorro se mueve a `(x, y)` donde había un conejo en el snapshot, el conejo queda sobreescrito en `nueva`. Luego, en el Paso 4, el conejo en la snapshot pasa por esta verificación:
```python
if type(nueva[i][j]) is dict and nueva[i][j]['tipo'] == 'zorro':
    continue  # se saltea sin registrar la muerte
```
El conejo muere sin que su edad se agregue a `edades_conejos_muertos`. El enunciado dice que la edad debe registrarse ("se registra la edad del conejo"). Esto incumple ese requisito y hace que las estadísticas del ejercicio 2 sean inexactas.

### Cómo corregirlo
Eliminar las líneas 143–144 de `mover_y_reproducir_zorros` (no corresponden al Paso 3). En cambio, en `mover_y_reproducir_conejos`, agregar el registro para el caso en que ya haya un zorro en la celda original del conejo:
```python
if type(nueva[i][j]) is dict and nueva[i][j]['tipo'] == 'zorro':
    edades_conejos_muertos.append(celda['edad'])  # registrar la muerte
    continue
```

---

## Error 3 — INCORRECTO: Valor de retorno de `simular_turno` no se desempaqueta

**Archivos:** `ejercicio_1.py` línea 22, `ejercicio_2.py` línea 22
**Severidad:** MEDIO — no crashea, pero el código es incorrecto

### Qué dice el código (ambos archivos)
```python
grilla_final = simular_turno(N, grilla_actual, ...)
```

### Por qué no funciona
`simular_turno` retorna una tupla de 3 elementos:
```python
return grilla, edades_zorros_muertos, edades_conejos_muertos
```
`grilla_final` recibe la tupla entera, no solo la grilla. No crashea porque `grilla_final` no se usa después, pero es incorrecto. En `ejercicio_3.py` esto se hace bien:
```python
grilla_final, edades_c, edades_z = simular_turno(...)  # ← correcto
```

### Cómo corregirlo
```python
grilla_final, _, _ = simular_turno(N, grilla_actual, ...)
```

---

## Error 4 — RIESGO: `NameError` posible si las listas de muertes están vacías

**Archivo:** `ejercicio_2.py`, líneas 23–29
**Severidad:** MEDIO — puede crashear; además viola el formato de output exigido

### Qué dice el código
```python
if len(edades_conejos_muertos) > 0:
    esperanza_conejo = sum(edades_conejos_muertos) / len(edades_conejos_muertos)
if len(edades_zorros_muertos) > 0:
    esperanza_zorro = sum(edades_zorros_muertos) / len(edades_zorros_muertos)
print(f'Esperanza de vida del conejo: {esperanza_conejo:.2f} turnos')
print(f'Esperanza de vida del zorro: {esperanza_zorro:.2f} turnos')
```

### Por qué no funciona
Si alguna lista está vacía, la variable (`esperanza_conejo` o `esperanza_zorro`) nunca se asigna → `NameError` al llegar al `print`.

### Qué exige el enunciado
El enunciado pide exactamente tres líneas de output. Un crash produce cero líneas y rompe el programa.

### Cómo corregirlo
Mover los `print` dentro de cada bloque `if`, o inicializar las variables antes:
```python
esperanza_conejo = sum(edades_conejos_muertos) / len(edades_conejos_muertos) if edades_conejos_muertos else 0
esperanza_zorro = sum(edades_zorros_muertos) / len(edades_zorros_muertos) if edades_zorros_muertos else 0
```

---

## Error 5 — PERFORMANCE: La simulación no para al extinguirse cuando `animar=False`

**Archivo:** `funciones_limpio.py`, líneas 249–256
**Severidad:** BAJO — no afecta la correctitud del output, pero impacta fuertemente el tiempo

### Qué dice el código
```python
if conejos == 0 and animar:
    print('Los conejos se extinguieron.')
    break
elif zorros == 0 and animar:
    print('Los zorros se extinguieron.')
    break
```

### Por qué es un problema
El `break` solo se alcanza si `animar=True`. Con `animar=False` (ejercicios 2 y 3), el loop corre siempre los 200 turnos aunque la extinción ocurra en el turno 5.

### Impacto en tiempo de ejecución
- Ejercicio 2: 100 simulaciones de 200 turnos = hasta 20.000 iteraciones de grilla 25×25 innecesarias
- Ejercicio 3: 20 valores de `dz` × 50 simulaciones × 200 turnos = hasta 200.000 iteraciones innecesarias

### Cómo corregirlo
```python
if conejos == 0:
    if animar:
        print('Los conejos se extinguieron.')
    break
elif zorros == 0:
    if animar:
        print('Los zorros se extinguieron.')
    break
```

---

## Resumen final

| # | Archivo | Línea(s) | Severidad | Descripción | ¿Incumple el enunciado? |
|---|---|---|---|---|---|
| 1 | `ejercicio_3.py` | 29 | CRÍTICO | `contar_animales` sin `N` → crash | Sí — el ejercicio no produce output |
| 2 | `funciones_limpio.py` | 143 + muertes no registradas | ALTO | Código muerto en paso equivocado; conejos muertos por zorro en Paso 3 no se cuentan | Sí — el enunciado exige registrar la edad |
| 3 | `ejercicio_1.py`, `ejercicio_2.py` | 22 | MEDIO | Retorno de `simular_turno` no desempaquetado | No produce crash, pero código incorrecto |
| 4 | `ejercicio_2.py` | 23–29 | MEDIO | `NameError` potencial si listas vacías | Sí — rompe el output de 3 líneas exigido |
| 5 | `funciones_limpio.py` | 249–256 | BAJO | No para la simulación al extinguirse sin animación | No directamente, pero afecta el tiempo de ejecución |
