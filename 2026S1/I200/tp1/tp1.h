#include <stdbool.h>

#ifndef TP0_TP0_C_H
#define TP0_TP0_C_H

typedef int** Matriz;

/*
 * Determina si dos numeros son amigos. Dos numeros son amigos si la suma de los divisores propios de cada uno es igual al otro numero.
 * Por ejemplo: 220 y 284 son amigos, ya que los divisores de 220 son 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 y 110 que suma 284.
 * Los divisores de 284 son 1, 2, 4, 71, 142 que suman 220. 
 * Nota: Los numeros iguales no se consideran amigos.
 */
bool are_friends_numbers(int x, int y);

/*
 * Dado la distancia inicial en metros, la distancia final en metros y la velocidad en metros por segundo de una particula, 
 * calcular el tiempo en segundos enteros del movimiento rectilineo uniforme.
 */
int calculate_time_in_seconds(float di, float df, float v) ;

/*
 * Intercambia dos valores de enteros.
 */
void swap(int *x, int *y);

/*
 * Devuelve el minimo indice de un arreglo de enteros. Si hay varios minimos, devuelve el menor indice
 */
int array_min_index(const int *array, int length);

/*
 * Copia un arreglo de enteros en memoria dinámica.
 * Si el arreglo es NULL devuelve NULL.
 */
 int *copy_array(const int *array, int length);

/*
 * Hace selection sort sobre un arreglo de enteros ascendentemente.
 * Si el arreglo es NULL, no hace nada.
 */
void selection_sort(int *array, int length);

/*
* Dado dos arreglos de enteros sin repetidos, queremos devolver un arreglo que sea la union de ambos arreglos de forma ordenada.
* La union no debe tener repetidos.
*/

int* array_union(const int *array1, int length1,
    const int *array2, int length2);

/*
 * Aplica la función a cada elemento de una matriz de enteros.
 */
void matrix_map(Matriz matrix, int row_size, int col_size, int f(int));

/*
 * Determina si dos matrices de enteros son identicamente iguales.
 * En el caso de que alguno sea NULL solo devuelve true si solo si el otro tambien lo es.
 */
bool matrix_equal(const Matriz matrix1, int row_size1, int col_size1, const Matriz matrix2, int row_size2, int col_size2);

/*
 * Devuelve una copia de una matriz de tamaño MxN.
 * En el caso de que sea NULL, tambien devuelve NULL.
 */
Matriz copy_matrix(const Matriz matrix, int row_size, int col_size);

/*
 * Copia un arreglo de matrices de enteros en memoria dinámica.
 * Si alguno de ellos en NULL, continua siendo NULL.
 * Si el arreglo de matrices es NULL, devuelve NULL.
 *
 * array_of_matrices: un arreglo de punteros a matrices de enteros.
 * matrix_dimensions: una matriz de 2xN, donde cada fila tiene dos valores, el tamaño de la fila y columna de la matriz correspondiente en array_of_matrices.
 * array_lenght: la cantidad de matrices.
 */
 Matriz* copy_array_of_matrices(const Matriz* array_of_matrices, const Matriz matrix_dimensions, int array_lenght);

/*
 * Libera toda la memoria asociada a un arreglo de matrices.
 *
 * array_of_matrices: un arreglo de punteros a matrices de enteros.
 * matrix_dimensions: una matriz de 2xN, donde cada fila tiene dos valores, el tamaño de la fila y columna de la matriz correspondiente en array_of_matrices.
 * array_amount: la cantidad de matrices.
 */
void free_array_of_matrices(Matriz *array_of_matrices, Matriz matrix_dimensions, int array_lenght);


#endif //TP0_TP0_C_H
