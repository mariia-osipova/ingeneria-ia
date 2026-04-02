#include "tp1.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int sum_of_devisors(int k) {
    int i = 2;
    int sum = 1;

    while (i < k) {
        if (k % i == 0) sum += i;
        i++;
    }
    return sum;
}

bool are_friends_numbers(int x, int y) {
    if (x == y) return false;

//    int sum_of_devisors(int k) {
//        int i = 2;
//        int sum = 1;
//
//        while (i < k) {
//            if (k % i == 0) sum += i;
//            i++;
//        }
//        return sum;
//    }

    if (sum_of_devisors(x) == y && sum_of_devisors(y) == x) return true;
    return false;
}

int calculate_time_in_seconds(float di, float df, float v) {
    // t = S/v
    if (v == 0.0) return -1; //caso borde devuelvo un error
    return ((abs((int)(df - di))) / (int)v);
}

void swap(int *x, int *y) {
    int aux = *x;
    *x = *y;
    *y = aux;
}

int array_min_index(const int *array, int length) {
    if (!array) return -1;
    int min = array[0];
    int menor_indice = 0;

    for (int i = 0; i < length; i++) {
        if (array[i] < min) {
            min = array[i];
            menor_indice = i;
        }
        else if (array[i] == min) {
            if (i < menor_indice) menor_indice = i;
        }
    }

    return menor_indice;
}

int *copy_array(const int *array, int length) {
    if (!array) return NULL;
    int *aux = (int *)malloc(sizeof(int)*length);

    for (int i = 0; i < length; i++) {
        aux[i] = array[i];
    }

    return aux;
}

void selection_sort(int *array, int length){
    if (!array || length < 2) return;

    for(int i = 0; i < length - 1; i++){
      int *min = &array[i];

      for(int j = i+1; j <= length - 1; j++){
        if (array[j] < *min) min = &array[j];
      }
      swap(&array[i], min);
    }
}

// ok voy a expicar ahora como hago la union abajo: primero que nada, tengo varias opciones:
// opcion 1.
// 1) puedo primero unir los dos arreglos - O(n)
// 2) despues sortear lo que me quedo O((n + m) log (n + m)) (uso merge sort porque es mas eficiente que selection sort (O(n^2)).
// podria haber usado la selection sort que ya tengo hecho, pero quiero implementar la funcion que sea lo mas linda y eficiente posible)
// 3) sacar las repeticiones O(n + m)
// --> me queda O((n + m) log (n + m))
// opcion 2.
// 1) ordeno cada uno O(n log n), O(m log m)
// 2) voy uniendo con dos punteros, aca tengo control directo a las repeticiones O(n + m)
// 3) optengo mi arr
// --> me queda O(n log n + m log m)
// O(n log n + m log m) < O((n + m) log (n + m)) para todos n, m > 0
// asi que eleji la opcion 2 con merge sort

typedef struct {
    int left;
    int right;
} SplitLength;

SplitLength split_length(int length) {
    SplitLength s;

    s.left = length / 2;
    s.right = length - s.left;

    return s;
}

int* merge(int* left, int length_l, int* right, int length_r) { //O(n)
    int *array_new = (int *)malloc(sizeof(int)*(length_l + length_r));

    int i = 0;
    int j = 0;
    int k = 0;

    while (i < length_l && j < length_r){
        if (left[i] < right[j]){
            array_new[k] = left[i];
            i ++;
        }
        else if (left[i] > right[j]){
            array_new[k] = right[j];
            j ++;
        }
        else {
          array_new[k] = left[i];
          i ++;
          j ++;
        }
        k ++;
    }

    // si me quedan elementos en left los meto
    // si me quedan elementos en right los meto

    if (i == length_l){
      while(j <= length_r - 1){
          array_new[k] = right[j];
          k++;
          j++;
      }
    }
    else if (j == length_r){
       while(i <= length_l - 1){
           array_new[k] = left[i];
           k++;
           i++;
       }
    }

    return array_new;
}

int* array_merge_sort(const int *array, int length){ //no puedo pasar int*. tengo que pasar const int*
  if (array == NULL || length == 0) return NULL;
  if (length == 1){
    int *single = (int*)malloc(sizeof(int));
    single[0] = array[0];
    return single;
  }

  int *array_copy = copy_array(array, length); // hago copy porque no puedo trabajar con el original
//  int *array_copy = (int *)malloc(sizeof(int)*i);

  SplitLength s = split_length(length);

  int length_l = s.left;
  int length_r = s.right;

  int *left  = &array_copy[0];
  int *right = &array_copy[length_l];

  left = array_merge_sort(left, length_l);
  right = array_merge_sort(right, length_r);

  int *result = merge(left, length_l, right, length_r);

  free(left);
  free(right);
  free(array_copy);

  return result;
}

int* array_union(const int *array1, int length1, const int *array2, int length2) {

  int *array1_copy_temp = copy_array(array1, length1);
  int *array2_copy_temp = copy_array(array2, length2);

  int *array1_sorted = array_merge_sort(array1_copy_temp, length1);
  int *array2_sorted = array_merge_sort(array2_copy_temp, length2);

  free(array1_copy_temp);
  free(array2_copy_temp);

  int *arr_new = merge(array1_sorted, length1, array2_sorted, length2);

  free(array1_sorted);
  free(array2_sorted);

  return arr_new;
}

void matrix_map(Matriz matrix, int row_size, int col_size, int f(int)) {
  if (matrix == NULL || f == NULL) return;

  for (int i = 0; i < row_size; i++) {
  	for (int j = 0; j < col_size; j++) matrix[i][j] = f(matrix[i][j]);
  }
  return;
}

Matriz copy_matrix(const Matriz matrix, int row_size, int col_size) {
    if (matrix == NULL) return NULL;
    Matriz matrix_new = (int**)malloc(sizeof(int*)*row_size);
    for (int i = 0; i < row_size; i++) matrix_new[i] = copy_array(matrix[i], col_size);
    return matrix_new;
}

bool matrix_equal(const Matriz matrix1, int row_size1, int col_size1, const Matriz matrix2, int row_size2, int col_size2) {
   if (matrix1 == NULL && matrix2 == NULL) return true;
   if (matrix1 == NULL || matrix2 == NULL) return false;
   if (row_size1 != row_size2 || col_size1 != col_size2) return false;

   for (int i = 0; i < row_size1; i++){
     for (int j = 0; j < col_size1; j++){
       if (matrix1[i][j] != matrix2[i][j]) return false;
     }
   }
   return true;
}

Matriz* copy_array_of_matrices(const Matriz *array_of_matrices, const Matriz matrix_dimensions, int array_length) { // length or lenght??? lo cambie: lenght --> length

  if (array_of_matrices == NULL){
    return NULL;
  }

  Matriz *array_of_matrices_new = (Matriz*)malloc(sizeof(Matriz) * array_length);

  for (int i = 0; i < array_length; i++){
    array_of_matrices_new[i] = copy_matrix(array_of_matrices[i], matrix_dimensions[i][0], matrix_dimensions[i][1]);
  }

  return array_of_matrices_new;
}

void free_array_of_matrices(Matriz* array_of_matrices, Matriz matrix_dimensions, int array_length) {

    for (int i = 0; i < array_length; i++) {
        for (int j = 0; j < matrix_dimensions[i][0]; j++) {
            free(array_of_matrices[i][j]);
        }
        free(array_of_matrices[i]);
    }
    free(array_of_matrices);

    for (int i = 0; i < array_length; i++) {
    free(matrix_dimensions[i]);
    }
    free(matrix_dimensions);

    return;
}