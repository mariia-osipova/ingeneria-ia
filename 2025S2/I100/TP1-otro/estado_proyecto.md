# Estado del proyecto — verificado contra el enunciado

---

## Fixes aplicados anteriormente

### Fix 1 — CRASH: `contar_animales` sin argumento `N` (`ejercicio_3 (1).py` línea 29)
**Problema:** `contar_animales(grilla_final)` — faltaba el argumento `N`.
Causaba `TypeError` en cada iteración. El ejercicio 3 nunca producía output.
**Fix:** `contar_animales(grilla_final, N)`

---

### Fix 2 — Zorros nunca ganaban energía al comer conejos (`funciones_limpio (1).py` línea 143)
**Problema:** La condición era `snapshot[x][y] == 'conejo'` — comparaba un
diccionario con un string, siempre `False`. Los zorros nunca ganaban `gz` energía.
**Fix:** `snapshot[x][y]['tipo'] == 'conejo'`

---

### Fix 3 — Retorno de `simular_turno` no desempaquetado (`ejercicio_1 (1).py` y `ejercicio_2 (1).py`)
**Problema:** `grilla_final = simular_turno(...)` — `simular_turno` retorna una
tupla de 3 elementos. `grilla_final` terminaba siendo una tupla en vez de una grilla.
**Fix:** `grilla_final, _, _ = simular_turno(...)`

---

### Fix 4 — `NameError` potencial en ejercicio 2 (`ejercicio_2 (1).py` líneas 23-29)
**Problema:** `esperanza_conejo` y `esperanza_zorro` se calculaban dentro de un `if`
pero se usaban en el `print` de afuera. Si las listas estaban vacías, las variables
nunca se asignaban → `NameError`.
**Fix:** Se movieron los `print` dentro de cada bloque `if/else`.

---

### Fix 5 — Simulación no paraba al extinguirse con `animar=False` (`funciones_limpio (1).py`)
**Problema:** El `break` de extinción estaba dentro de `if animar:`, así que con
`animar=False` (ejercicios 2 y 3) siempre corría los 200 turnos aunque todos los
animales estuvieran muertos desde el turno 10. Hasta 200.000 iteraciones innecesarias.
**Fix:** Se sacó el `break` del bloque `if animar:` para que se ejecute siempre.

---

### Fix 6 — Zorros comían conejos en el paso incorrecto (`funciones_limpio (1).py`)
**Problema:** En `mover_y_reproducir_zorros` (Paso 3), cuando un zorro se movía
a una celda con un conejo, el zorro ganaba `gz` energía. El enunciado dice que
la ganancia de energía ocurre en el Paso 4 (movimiento de conejos), no en el Paso 3.
Esto duplicaba la tasa de caza.
**Fix:** Se eliminó el bloque de ganancia de energía del Paso 3.

---

### Fix 7 — Muertes de conejos no registradas cuando el zorro se mueve a su celda (`funciones_limpio (1).py`)
**Problema:** Cuando un zorro se movía a una celda con conejo (Paso 3), el conejo
quedaba sobreescrito en `nueva`. En el Paso 4, al encontrar al conejo en el snapshot
con un zorro en `nueva`, el código hacía `continue` sin registrar la muerte.
La edad del conejo nunca se agregaba a `edades_conejos_muertos`, sesgando las
estadísticas del ejercicio 2.
**Fix:** Se agregó `edades_conejos_muertos.append(celda['edad'])` antes del `continue`
en `mover_y_reproducir_conejos`.

---

### Fix 8 — Animación brusca (`funciones_limpio (1).py`)
**Problema:** `print('\n' * 50)` empujaba la pantalla hacia abajo en cada turno
en vez de actualizar en su lugar, causando un efecto de salto.
**Fix:** `print('\033[H', end='', flush=True)` — mueve el cursor al inicio
sin limpiar la pantalla, eliminando el salto. *(Este fix se perdió y necesita reaplicarse.)*

---

## ejercicio_1 (1).py — ROTO ❌

**Problema: SyntaxError en línea 1**

El archivo tiene texto corrupto al inicio:
```
ejercicio_2 (1).pyfrom funciones_limpio import crear_grilla, simular_turno
```

Python no puede parsear el archivo. No corre en absoluto.

**Cómo debe quedar la línea 1:**
```python
from funciones_limpio import crear_grilla, simular_turno
```

---

## ejercicio_2 (1).py — OK ✓

Corre sin errores. Imprime exactamente 3 líneas como pide el enunciado:
```
Muertes registradas - Conejos: 64378 | Zorros: 48787
Esperanza de vida del conejo: 8.36 turnos
Esperanza de vida del zorro: 6.80 turnos
```

---

## ejercicio_3 (1).py — OK ✓

Corre sin errores. Tabla correcta con los 20 valores de `dz` (0.01 → 0.39, paso 0.02),
50 simulaciones por valor. Los resultados tienen sentido ecológico: a mayor densidad
de zorros, menor porcentaje de coexistencia.

Output de ejemplo:
```
+--------+---------------------+
|  d_z   |   Sin extinciones   |
+--------+---------------------+
| 0.01   |   74.00 %           |
+--------+---------------------+
| 0.03   |   86.00 %           |
+--------+---------------------+
...
| 0.39   |    0.00 %           |
+--------+---------------------+
```

---

## funciones_limpio (1).py — Funciona con 2 problemas menores ⚠️

### Problema 1: Animación sigue siendo brusca
Línea 241:
```python
print('\n' * 50)   # ← salta la pantalla en vez de actualizar en su lugar
```
Debe ser:
```python
print('\033[H', end='', flush=True)   # ← mueve el cursor al inicio sin limpiar
```
Este fix se aplicó antes pero se perdió cuando se copió el archivo.

### Problema 2: Listas globales no usadas
Líneas 6–7:
```python
edades_conejos_muertos = []
edades_zorros_muertos = []
```
Están definidas a nivel de módulo pero ninguna función las usa — todas reciben
estas listas como parámetros. Son código muerto que no causa errores pero
no debería estar.

---

## Nombre de archivos — no coincide con la convención del enunciado ⚠️

El enunciado pide:
```
tp1_funciones_apellido.py
tp1_1_apellido.py
tp1_2_apellido.py
tp1_3_apellido.py
```

Los archivos actuales se llaman `ejercicio_1 (1).py`, etc. Hay que renombrarlos
antes de entregar.

---

## Resumen

| Archivo | Estado | Problema |
|---|---|---|
| `ejercicio_1 (1).py` | ❌ ROTO | SyntaxError en línea 1, texto corrupto |
| `ejercicio_2 (1).py` | ✓ OK | — |
| `ejercicio_3 (1).py` | ✓ OK | — |
| `funciones_limpio (1).py` | ⚠️ Funciona | Animación brusca; listas globales sin usar |
| Nombres de archivos | ⚠️ Pendiente | No coinciden con la convención del enunciado |
