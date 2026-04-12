# Clase Tournament Heap y Busqueda Binaria
*Algoritmos y estructuras de datos*

## Ejercicio 1
**El segundo mejor**
En un **Tournament Tree** queremos implementar la primitiva **get_second_best()**, que devuelve el segundo mayor elemento en el árbol. Indique cuál es el peor caso para esta primitiva en un árbol de 8 elementos.

Ej: 

Input: [5,4,3,2,7]
Output: 5

## Ejercicio 2
**Cantidad de comparaciones**
Si tenemos un **Tournament Heap** de 64 elementos y hacemos un **remove_max()** seguido de **get_max()**, ¿Cuántas comparaciones hace el **get_max()** exactamente?


## Ejercicio 3
**Picos**: 
Decimos que un arreglo es una Montaña si se cumplen ambas condiciones:

1. El arreglo tiene al menos tres elementos (size >= 3)
2. A[0] <= A[1] <= A[2] <= .... <= A[k] >= A[k+1] >= A[k+2] >= .... >= A[size-1].

En este caso, decimos que el indice k es el PICO de la montaña.

Escribir un algoritmo para encontrar el pico de la Montaña en O(log n). Contamos con un parametro que nos dice el tamaño del array.

## Ejercicio 4
**Rotaciones**: 
Un arreglo ordenado fue rotado k posiciones sobre un pivote desconocido.
Dado un elemento target, encontrar su indice en el arreglo en O(log n). Contamos con un parametro que nos dice el tamaño del array

En caso de no existir, retornar -1.

## Ejercicio 5 (Extra)

Se tiene una fila de **N** habitaciones en un pasillo largo. Cada habitación **i** está en una posición **X_i** a lo largo de una línea recta (un eje **x**). Tenes **K** routers de Wi-Fi potentes y queres instalarlos en **K** de esas habitaciones de tal manera que la distancia mínima entre cualquier par de routers sea lo más grande posible.

Tu objetivo es encontrar esa distancia mínima maximizada.
