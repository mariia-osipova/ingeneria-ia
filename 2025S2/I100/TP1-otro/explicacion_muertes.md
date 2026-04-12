# El problema de las muertes no registradas — Explicación completa

---

## Contexto: ¿qué es `edades_conejos_muertos`?

Es una lista que acumula la **edad de cada conejo en el momento de su muerte**.
Al final de las 100 simulaciones (ejercicio 2), se usa para calcular la esperanza de vida:

```python
esperanza_conejo = sum(edades_conejos_muertos) / len(edades_conejos_muertos)
```

Si un conejo muere pero su edad **no se agrega a esta lista**, ese conejo no existe
para la estadística. El promedio calculado va a ser incorrecto.

---

## ¿Cuándo puede morir un conejo?

Hay exactamente **tres causas de muerte** para un conejo:

| # | Causa | ¿Quién se mueve? | ¿En qué paso? |
|---|---|---|---|
| 1 | Se queda sin energía (llega a 0) | Nadie, muere en su celda | Paso 2 |
| 2 | Camina hacia una celda con zorro | El **conejo** | Paso 4 |
| 3 | Un zorro camina hacia su celda | El **zorro** | Paso 3 |

El código registra bien la causa 1 y la causa 2. El problema es la **causa 3**.

---

## Causa 1 — Sin energía: registrada correctamente ✓

```python
conejo['energia'] = celda['energia'] - 1

if conejo['energia'] == 0:
    edades_conejos_muertos.append(conejo['edad'])  # ← se registra ✓
```

Fácil: si la energía llega a 0, se agrega la edad a la lista. Sin problema.

---

## Causa 2 — Conejo camina hacia zorro: registrada correctamente ✓

```python
# En mover_y_reproducir_conejos
# El conejo está en (i,j) y eligió moverse a (x,y)
# En (x,y) hay un zorro en la nueva grilla

if es_zorro:
    nueva[x][y]['energia'] += gz                   # el zorro come, gana energía
    edades_conejos_muertos.append(conejo['edad'])  # ← se registra ✓
```

Acá también está bien. El conejo intentó moverse, encontró un zorro, murió,
y su edad quedó registrada.

Notá que en este momento `conejo` **ya existe como diccionario** porque fue
construido unas líneas antes:

```python
conejo = {}
conejo['tipo'] = 'conejo'
conejo['energia'] = celda['energia'] - 1
conejo['edad'] = celda['edad'] + 1    # ← edad actualizada, disponible para usar
```

---

## Causa 3 — Zorro camina hacia el conejo: ¡NO registrada! ✗

Este es el caso problemático. Mirá qué pasa paso a paso.

### Paso 3: el zorro se mueve

En `mover_y_reproducir_zorros`, el zorro en `(i,j)` elige moverse a `(x,y)`.
En el snapshot, `(x,y)` tiene un conejo. El zorro lo pisa:

```python
if type(snapshot[x][y]) is dict and snapshot[x][y]['tipo'] == 'conejo':
    zorro['energia'] += gz    # el zorro gana energía (esto está en el paso incorrecto
                              # según el enunciado, pero al menos hace algo)
nueva[x][y] = zorro           # el zorro se mueve → el conejo queda SOBREESCRITO
                              # en la nueva grilla. Desaparece. Pero su edad
                              # NUNCA se agrega a edades_conejos_muertos ✗
```

El conejo murió. Nadie lo sabe. La lista no se enteró.

### Paso 4: procesando ese mismo conejo

Ahora llega el turno de `mover_y_reproducir_conejos`. La función itera el
snapshot buscando conejos. Encuentra al conejo en `(x,y)` (sigue en el snapshot
porque el snapshot es una copia del turno anterior).

```python
celda = snapshot[i][j]   # i,j = x,y del ejemplo anterior
                         # celda = {'tipo': 'conejo', 'energia': 4, 'edad': 7}
                         # el conejo SÍ aparece en el snapshot

if type(celda) is dict and celda['tipo'] == 'conejo':   # ← entra acá, es un conejo

    if type(nueva[i][j]) is dict and nueva[i][j]['tipo'] == 'zorro':
        continue   # ← SALE INMEDIATAMENTE
                   # nueva[i][j] tiene un zorro porque el zorro se movió ahí en Paso 3
                   # el código dice "ah, ya hay un zorro, me salteo este conejo"
                   # y se va sin registrar nada
```

Ese `continue` hace que el loop pase al siguiente conejo **sin ejecutar ninguna
otra línea**. La variable `conejo` nunca se construye. La lista nunca se actualiza.

---

## Visualización del problema

Imaginá este estado antes del turno:

```
Snapshot (turno anterior):     Nueva grilla (se va construyendo):

  A   B   C                      A   B   C
+---+---+---+                  +---+---+---+
| Z |   |   |   fila 0         |   |   |   |   fila 0
+---+---+---+                  +---+---+---+
|   | C |   |   fila 1         |   | C |   |   fila 1  ← conejo todavía acá
+---+---+---+                  +---+---+---+
|   |   |   |   fila 2         |   |   |   |   fila 2
+---+---+---+                  +---+---+---+

Z = zorro en (0,A)
C = conejo en (1,B)
```

**Durante Paso 3** — el zorro en `(0,A)` elige moverse a `(1,B)` (donde está el conejo):

```
Nueva grilla después del Paso 3:

  A   B   C
+---+---+---+
|   |   |   |   fila 0   ← (0,A) queda vacío (el zorro se fue)
+---+---+---+
|   | Z |   |   fila 1   ← (1,B) ahora tiene el zorro
+---+---+---+            ← el conejo fue sobreescrito. Desapareció.
|   |   |   |   fila 2
+---+---+---+
```

**Durante Paso 4** — el código procesa el snapshot y encuentra al conejo en `(1,B)`:

```python
celda = snapshot[1][B]   # {'tipo': 'conejo', 'energia': 4, 'edad': 7}
# entra al if de conejo...
nueva[1][B]              # {'tipo': 'zorro', ...}   ← hay un zorro acá
# → continue. El conejo se saltea. Nadie registra su muerte.
```

---

## ¿Por qué es un problema para las estadísticas?

Supongamos que en 100 simulaciones hay 5000 muertes de conejos reales.
Si 1500 de ellas son de tipo "zorro camina al conejo" (causa 3), la lista
`edades_conejos_muertos` solo va a tener 3500 entradas en vez de 5000.

El promedio calculado va a ser incorrecto porque:
- Faltan muertes → el denominador es más chico de lo real
- Las muertes que faltan son probablemente de conejos jóvenes (los que no
  tuvieron tiempo de escapar del zorro) → el promedio va a parecer más alto
  de lo real, sesgando los resultados

---

## La causa raíz en una oración

Cuando el zorro llega al conejo, el código dice *"ya hay un zorro, me salteo
este conejo"* — pero antes de saltear, **nadie anotó que el conejo murió**.

---

## ⚠️ Importante: solo UN lugar para registrar, no dos

Puede parecer lógico registrar la muerte en los DOS lugares (Paso 3 y Paso 4),
pero eso sería un **error**: el mismo conejo quedaría contado dos veces en
`edades_conejos_muertos`, distorsionando la esperanza de vida.

El Paso 3 y el Paso 4 están procesando **el mismo conejo** — uno cuando el
zorro llega a su celda, y el otro cuando el loop de conejos lo encuentra en
el snapshot y lo saltea. Son dos puntos de vista del mismo evento.

---

## La solución correcta: elegir UNO de estos dos enfoques

### Opción A — registrar en Paso 3 (donde la muerte realmente ocurre)

```python
# En mover_y_reproducir_zorros
# ANTES:
if type(snapshot[x][y]) is dict and snapshot[x][y]['tipo'] == 'conejo':
    zorro['energia'] += gz    # wrong step, no death recorded
nueva[x][y] = zorro

# DESPUÉS:
if type(snapshot[x][y]) is dict and snapshot[x][y]['tipo'] == 'conejo':
    edades_conejos_muertos.append(snapshot[x][y]['edad'])  # ← registrar acá
nueva[x][y] = zorro
# El continue en Paso 4 queda igual, sin cambios
```

Se usa `snapshot[x][y]['edad']` porque es el conejo del snapshot. No existe
ningún diccionario `conejo` construido en esta función.

### Opción B — registrar en Paso 4 (más limpio, todo centralizado)

```python
# En mover_y_reproducir_conejos
# ANTES:
if type(nueva[i][j]) is dict and nueva[i][j]['tipo'] == 'zorro':
    continue

# DESPUÉS:
if type(nueva[i][j]) is dict and nueva[i][j]['tipo'] == 'zorro':
    edades_conejos_muertos.append(celda['edad'])  # ← registrar acá
    continue
# El Paso 3 queda igual (solo se elimina el energy gain)
```

Se usa `celda['edad']` (no `conejo['edad']`) porque `conejo` todavía no fue
construido — el `continue` ocurre antes de esas líneas.

### ¿Cuál elegir?

**Opción B es más prolija** — toda la lógica de muerte de conejos queda dentro
de `mover_y_reproducir_conejos`. Es más fácil de leer y mantener.

La Opción A también es correcta, pero divide la responsabilidad entre dos funciones.

---

## Resumen visual de los tres casos

```
MUERTE 1: sin energía
  celda → conejo construido → energia == 0 → append(conejo['edad']) ✓

MUERTE 2: conejo camina al zorro
  celda → conejo construido → destino tiene zorro → append(conejo['edad']) ✓

MUERTE 3: zorro camina al conejo
  Paso 3: zorro sobreescribe conejo en nueva → append(snapshot[x][y]['edad']) ← falta
  Paso 4: celda es conejo, nueva tiene zorro → continue               ← falta append(celda['edad'])
```
