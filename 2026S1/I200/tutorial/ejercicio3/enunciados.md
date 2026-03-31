# Ejercicios de Listas Enlazadas

## Ejercicio 1 — Largo de una lista

Dada una lista enlazada simple, implementar una función que devuelva la cantidad de nodos que contiene.

**Firma:** `int length(Node *list)`

**Ejemplo:**
```
Entrada: 1 -> 2 -> 3 -> 4 -> 5
Salida:  5
```

---

## Ejercicio 2 — Nodo del medio

Dada una lista enlazada simple, implementar una función que devuelva el nodo del medio **en un solo recorrido** de la lista, sin usar memoria adicional ni conocer su largo de antemano.

Si la lista tiene una cantidad par de nodos, devolver el segundo nodo del medio.

**Firma:** `Node *middle_node(Node *list)`

**Ejemplos:**
```
Entrada: 1 -> 2 -> 3 -> 4 -> 5     Salida: nodo(3)
Entrada: 1 -> 2 -> 3 -> 4          Salida: nodo(3)
```

---

## Ejercicio 3 — Detección de ciclo

Dada una lista enlazada simple que puede contener un ciclo, implementar una función que devuelva `1` si la lista tiene ciclo y `0` en caso contrario. La solución no debe usar memoria adicional.

**Firma:** `int has_cycle(Node *list)`

**Ejemplos:**
```
Entrada: 1 -> 2 -> 3 -> 4 -> 5 -> NULL          Salida: 0
Entrada: 1 -> 2 -> 3 -> 4 -> 5 -> (vuelve a 3)  Salida: 1
```

---

## Ejercicio 4 — Intersección de listas ordenadas

Dadas dos listas enlazadas simples ordenadas, implementar una función que devuelva una nueva lista ordenada con los elementos que aparecen en ambas listas.

**Firma:** `Node *sorted_intersection(Node *a, Node *b)`

**Ejemplo:**
```
Entrada a: 1 -> 3 -> 5 -> 7 -> 9
Entrada b: 2 -> 3 -> 5 -> 6 -> 9 -> 10
Salida:    3 -> 5 -> 9
```
