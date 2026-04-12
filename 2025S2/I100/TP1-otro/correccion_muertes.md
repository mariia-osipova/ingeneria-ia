# Corrección: el error en mi explicación anterior

---

## El error que cometí

En `explicacion_muertes.md` sugerí **dos cambios** al mismo tiempo:
- Cambio 1: registrar la muerte en `mover_y_reproducir_zorros` (Paso 3)
- Cambio 2: registrar la muerte en `mover_y_reproducir_conejos` (Paso 4)

Esto está **mal**. Los dos cambios juntos registrarían la misma muerte **dos veces**.

---

## Por qué sería doble conteo

Cuando un zorro se mueve a la celda de un conejo, hay dos momentos en el código
donde ese conejo aparece:

1. **Paso 3** — `mover_y_reproducir_zorros`: el zorro sobreescribe al conejo en `nueva`
2. **Paso 4** — `mover_y_reproducir_conejos`: el loop encuentra al conejo en el snapshot
   y ejecuta `continue` porque ya hay un zorro en `nueva`

Son dos puntos de vista del **mismo evento** — el mismo conejo, la misma muerte.
Si registrás en ambos lugares, ese conejo aparece dos veces en `edades_conejos_muertos`.

---

## Lo que dice el enunciado

> "Si su celda destino tiene un zorro (en la nueva grilla): el zorro come al conejo,
> gana gz puntos de energía, **y se registra la edad del conejo**"

Esto describe el Paso 4 (movimiento de conejos). El enunciado **no dice nada** sobre
qué pasa cuando el zorro se mueve a una celda con conejo en el Paso 3 — solo habla
de registrar la muerte cuando el conejo camina hacia el zorro.

---

## La solución correcta: solo UN cambio

Hay dos opciones válidas. Solo implementás una, no las dos.

---

### Opción A — registrar en Paso 3

En `mover_y_reproducir_zorros`, reemplazás la ganancia de energía por el registro
de la muerte:

```python
# ANTES (buggy):
if type(snapshot[x][y]) is dict and snapshot[x][y]['tipo'] == 'conejo':
    zorro['energia'] += gz    # ganancia de energía en el paso incorrecto
nueva[x][y] = zorro           # conejo sobreescrito, muerte no registrada

# DESPUÉS (fix):
if type(snapshot[x][y]) is dict and snapshot[x][y]['tipo'] == 'conejo':
    edades_conejos_muertos.append(snapshot[x][y]['edad'])  # muerte registrada
nueva[x][y] = zorro
```

El `continue` en Paso 4 queda **sin cambios**.

Por qué `snapshot[x][y]['edad']` y no otra cosa: el conejo está en la celda
`(x,y)` del snapshot. No hay ningún diccionario `conejo` disponible en esta
función — esa variable no existe acá.

---

### Opción B — registrar en Paso 4 (más recomendable)

En `mover_y_reproducir_conejos`, agregás el registro justo antes del `continue`:

```python
# ANTES (buggy):
if type(nueva[i][j]) is dict and nueva[i][j]['tipo'] == 'zorro':
    continue

# DESPUÉS (fix):
if type(nueva[i][j]) is dict and nueva[i][j]['tipo'] == 'zorro':
    edades_conejos_muertos.append(celda['edad'])  # muerte registrada
    continue
```

El código del Paso 3 queda **sin cambios** (excepto eliminar la ganancia de energía).

Por qué `celda['edad']` y no `conejo['edad']`: el diccionario `conejo` todavía
no fue construido cuando se ejecuta este `continue`. El `continue` está ANTES
de las líneas que construyen `conejo`. En cambio, `celda = snapshot[i][j]` ya
está disponible — es el conejo del snapshot.

```python
celda = snapshot[i][j]   # ← ya existe, tiene la edad del conejo

if type(nueva[i][j]) is dict and nueva[i][j]['tipo'] == 'zorro':
    edades_conejos_muertos.append(celda['edad'])  # ← usás celda acá
    continue

conejo = {}              # ← conejo recién se construye DESPUÉS del continue
conejo['edad'] = celda['edad'] + 1
```

---

### ¿Cuál elegir?

| | Opción A | Opción B |
|---|---|---|
| Dónde se registra | Paso 3 (zorro se mueve) | Paso 4 (conejo es procesado) |
| Consistencia con el enunciado | La muerte ocurre en el Paso 3, pero el enunciado no lo menciona | Más alineada con cómo el enunciado describe el Paso 4 |
| Organización del código | Divide responsabilidad entre dos funciones | Todo el registro de muertes de conejos queda en una sola función |
| Recomendación | ✓ funciona | ✓✓ más prolijo |

**Recomendación: Opción B** — es más consistente con el enunciado y mantiene
toda la lógica de muerte de conejos dentro de `mover_y_reproducir_conejos`.
