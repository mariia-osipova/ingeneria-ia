# Reporte Final — TP1 Circle of Life

---

## Lo que funciona correctamente ✓

- Todos los parámetros coinciden exactamente con el enunciado: N=25, dc=0.12, dz=0.20, dp=0.35, ec=5, ez=12, gc=4, gz=8, pp=0.50, prc=0.18, prz=0.18, e_min=4, Tmax=200
- `crear_grilla` — genera la grilla correctamente con las densidades indicadas
- `vecinos` — vecindad de Von Neumann (4 vecinos), maneja bordes correctamente
- `crecer_pasto` — lee del snapshot, crece solo en celdas `None`, usa probabilidad pp
- `contar_animales` — cuenta correctamente ambas especies
- `elegir_destino_zorro` — evita celdas con zorros en el snapshot ✓
- `elegir_destino_conejo` — evita celdas con cualquier animal en el snapshot ✓
- Movimiento de zorros y conejos — lógica correcta
- Reproducción — condiciones correctas (energía >= e_min, probabilidades, cría en celda original)
- Snapshot usado correctamente para todas las decisiones de movimiento ✓
- Terminación anticipada al extinguirse una especie ✓
- `ejercicio_2` — 100 simulaciones, imprime exactamente 3 líneas ✓
- `ejercicio_3` — rango dz correcto (0.01→0.39, paso 0.02, 20 valores), 50 simulaciones por valor, tabla correcta ✓
- Colores correctos: verde=pasto, cyan=conejo, rojo=zorro ✓
- Solo usa librerías permitidas: `termcolor`, `random`, `time` ✓

---

## Problemas pendientes

### 1 — CRÍTICO: `ejercicio_1 (1).py` no corre

**Archivo:** `ejercicio_1 (1).py`, línea 1

El archivo tiene texto corrupto al inicio:
```
ejercicio_2 (1).pyfrom funciones_limpio import crear_grilla, simular_turno
```
Python no puede parsear el archivo. Tira `SyntaxError` inmediatamente.

**Cómo debe ser la línea 1:**
```python
from funciones_limpio import crear_grilla, simular_turno
```

---

### 2 — ALTO: Nombres de archivo no coinciden con la convención del enunciado

**El enunciado pide:**
```
tp1_funciones_apellido.py
tp1_1_apellido.py
tp1_2_apellido.py
tp1_3_apellido.py
```

**Archivos actuales:**
```
funciones_limpio (1).py
ejercicio_1 (1).py
ejercicio_2 (1).py
ejercicio_3 (1).py
```

Hay que renombrarlos antes de entregar, reemplazando `apellido` con tu apellido real.

---

### 3 — MEDIO: Inconsistencia en la edad registrada al morir comido por un zorro

**Archivo:** `funciones_limpio (1).py`, líneas 178 y 202

Hay dos escenarios donde un conejo muere comido por un zorro. El problema es que
registran la edad de manera inconsistente:

**Escenario A — el zorro se mueve a la celda del conejo (línea 178):**
```python
edades_conejos_muertos.append(celda['edad'])   # edad SIN el incremento del turno actual
```

**Escenario B — el conejo se mueve a la celda del zorro (línea 202):**
```python
edades_conejos_muertos.append(conejo['edad'])  # conejo['edad'] = celda['edad'] + 1
                                               # edad CON el incremento del turno actual
```

El mismo evento (conejo comido por zorro) registra una edad diferente dependiendo
de quién se movió. El escenario A siempre registra 1 turno menos que el B.

**Por qué importa:** sesga ligeramente la esperanza de vida del conejo en ejercicio 2.

**Fix:** hacer que ambos registren la misma cosa. La opción más consistente es
usar `celda['edad'] + 1` en ambos (la edad incluyendo el turno en que murió):

```python
# línea 178 — escenario A
edades_conejos_muertos.append(celda['edad'] + 1)  # sumar 1 para ser consistente con B
```

---

### 4 — MEDIO: Animación sigue siendo brusca

**Archivo:** `funciones_limpio (1).py`, línea 241

```python
print('\n' * 50)   # ← empuja la pantalla hacia abajo en cada turno
```

Este fix se aplicó anteriormente pero se perdió. Debe ser:
```python
print('\033[H', end='', flush=True)   # ← mueve el cursor al inicio sin saltar
```

---

### 5 — BAJO: Dos archivos `funciones_limpio` en el directorio

El directorio tiene tanto `funciones_limpio.py` como `funciones_limpio (1).py`.
Solo `funciones_limpio.py` es importado (Python no puede importar archivos con
espacios en el nombre). El archivo `(1)` es código muerto que no se usa.
Conviene eliminarlo antes de entregar para no confundir.

---

### 6 — BAJO: Listas globales sin usar en `funciones_limpio (1).py`

Líneas 6–7:
```python
edades_conejos_muertos = []
edades_zorros_muertos = []
```
Están definidas a nivel de módulo pero ninguna función las usa — todas reciben
estas listas como parámetros. Son código muerto inofensivo pero innecesario.

---

## Resumen de prioridades

| # | Severidad | Qué hacer |
|---|---|---|
| 1 | CRÍTICO | Corregir línea 1 de `ejercicio_1 (1).py` |
| 2 | ALTO | Renombrar todos los archivos a `tp1_N_apellido.py` antes de entregar |
| 3 | MEDIO | Unificar el registro de edad en las dos rutas de muerte por depredación |
| 4 | MEDIO | Re-aplicar el fix de animación (`\033[H`) |
| 5 | BAJO | Eliminar `funciones_limpio (1).py` del directorio |
| 6 | BAJO | Eliminar listas globales sin usar en `funciones_limpio` |

---

## Fixes aplicados durante esta sesión (historial)

| Fix | Archivo | Descripción |
|---|---|---|
| 1 | `ejercicio_3 (1).py` | `contar_animales` faltaba argumento `N` → crash siempre |
| 2 | `funciones_limpio (1).py` | `snapshot[x][y] == 'conejo'` → `snapshot[x][y]['tipo'] == 'conejo'` |
| 3 | `ejercicio_1`, `ejercicio_2` | Retorno de `simular_turno` no desempaquetado |
| 4 | `ejercicio_2 (1).py` | `NameError` potencial si listas de muertes vacías |
| 5 | `funciones_limpio (1).py` | Extinción no cortaba la simulación con `animar=False` |
| 6 | `funciones_limpio (1).py` | Zorros ganaban energía en el Paso 3 (paso incorrecto según enunciado) |
| 7 | `funciones_limpio (1).py` | Muertes de conejos no registradas cuando el zorro se mueve a su celda |
| 8 | `funciones_limpio (1).py` | Animación brusca (`\n * 50` → `\033[H`) *(se perdió, pendiente reaplicar)* |
