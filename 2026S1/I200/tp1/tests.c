#include "testing.h"
#include "tp1.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

bool test_are_friends_numbers() {
  bool tests_result = true;

  tests_result &= test_assert("Prueba que 220 y 284 son amigos", are_friends_numbers(220, 284));
  tests_result &= test_assert("Prueba que 1184 y 1210 son amigos", are_friends_numbers(1184, 1210));
  tests_result &= test_assert("Prueba que 63020 y 76084 son amigos", are_friends_numbers(63020, 76084));
  tests_result &= test_assert("Prueba que 1184 y 1200 no son amigos", !are_friends_numbers(1184, 1200));
  tests_result &= test_assert("Prueba que 6 y 6 no son amigos", !are_friends_numbers(6, 6));
  tests_result &= test_assert("Prueba que 1 y 1 no son amigos", !are_friends_numbers(1, 1));
  tests_result &= test_assert("Prueba que 2 y 4 no son amigos", !are_friends_numbers(2, 4));

  return tests_result;
}

bool test_calculate_time_in_seconds() {
  bool tests_result = true;

  tests_result &= test_assert("Prueba de distancia 0", calculate_time_in_seconds(0.0f, 0.0f, 2.0f) == 0);
  tests_result &= test_assert("Prueba distancia 10 metros, velocidad 2 m/s", calculate_time_in_seconds(0.0f, 10.0f, 2.0f) == 5);
  tests_result &= test_assert("Prueba distancia 5 metros, velocidad 5 m/s", calculate_time_in_seconds(15.0f, 20.0f, 5.0f) == 1);
  tests_result &= test_assert("Prueba distancia 10 metros, velocidad 0 m/s", calculate_time_in_seconds(10.0f, 20.0f, 0.0f) == -1);
  tests_result &= test_assert("Prueba distancia 10 metros, velocidad 1 m/s", calculate_time_in_seconds(110.0f, 100.0f, 1.0f) == 10);
  tests_result &= test_assert("Prueba distancia 1000 metros, velocidad 100 m/s", calculate_time_in_seconds(0.0f, 1000.0f, 100.0f) == 10);

  return tests_result;
}

bool test_swap() {
  bool tests_result = true;
  int x = 4;
  int y = 5;

  swap(&x, &y);

  tests_result &=
      test_assert("Prueba swap enteros positivos", (x == 5 && y == 4));

  x = -1;
  y = 1;
  swap(&x, &y);
  tests_result &=
      test_assert("Prueba swap enteros con signo", (x == 1 && y == -1));

  x = 1;
  y = 1;
  swap(&x, &y);
  tests_result &=
      test_assert("Prueba swap enteros iguales", (x == 1 && y == 1));
  return tests_result;
}

bool test_array_min_index() {
  bool tests_result = true;
  int array[5];
  
  for (int i = 0; i < 5; i++) {
    array[i] = i;
  }
  tests_result &= test_assert("Prueba mínimo índice de arreglo", array_min_index(array, 5) == 0);

  for (int i = 0; i < 5; i++) {
    array[i] = 10 - i;
  }
  tests_result &= test_assert("Prueba mínimo índice de arreglo con números decrecientes", array_min_index(array, 5) == 4);

  for (int i = 0; i < 5; i++) {
    array[i] = 5;
  }
  tests_result &= test_assert("Prueba mínimo índice de arreglo con elementos iguales", array_min_index(array, 5) == 0);

  array[3] = 2;
  array[4] = 1;
  tests_result &= test_assert("Prueba mínimo índice de arreglo con un valor menor", array_min_index(array, 5) == 4);

  tests_result &= test_assert("Prueba mínimo índice de arreglo de un elemento", array_min_index(&array[2], 1) == 0);
  tests_result &= test_assert("Prueba mínimo índice de NULL", array_min_index(NULL, 0) == -1);

  array[1] = 1; 
  tests_result &= test_assert("Prueba varios mínimos devuelve de menor indice", array_min_index(array, 5) == 1);
  
  return tests_result;
}

bool compare_arrays(const int *array1, const int *array2, int length) {
  for (int i = 0; i < length; i++) {
    if (array1[i] != array2[i]) return false;
  }
  return true;
}

bool test_array_copy() {
  bool tests_result = true;
  bool test_result = true;
  int array[5];

  for (int i = 0; i < 5; i++) {
    array[i] = i;
  }
  int *copy = copy_array(array, 5);

  for (int i = 0; i < 5; i++) {
    test_result &= copy[i] == array[i];
    copy[i] = copy[i] * 2;
    test_result &= copy[i] == array[i] * 2;
  }
  tests_result &= test_assert("Prueba copiar arreglo", test_result);
  free(copy);
  tests_result &=
      test_assert("Prueba copiar arreglo nulo", !copy_array(NULL, 56));
  return tests_result;
}

bool test_selection_sort() {
  bool tests_result = true;
  bool test_result = true;
  int array[100];
  for (int i = 0; i < 100; i++) {
    array[i] = 99 - i;
  }

  selection_sort(NULL, 30);
  tests_result &= test_assert("Prueba selection sort sobre arreglo NULL", true);

  selection_sort(array, 100);

  for (int i = 0; i < 100; i++) {
    test_result &= array[i] == i;
  }

  tests_result &= test_assert("Prueba selection sort simple", test_result);
  test_result = true;

  for (int i = 0; i < 100; i++) {
    array[i] = -array[i];
  }
  selection_sort(array, 100);
  for (int i = 0; i < 100; i++) {
    test_result &= array[i] == -(99 - i);
  }
  tests_result &= test_assert("Prueba selection sort negativos", test_result);

  return tests_result;
}

bool test_array_union() {
  bool tests_result = true;

  int test1_array1[5] = {1, 3, 5, 7, 9};
  int test1_array2[4] = {2, 4, 6, 8};
  int expected_test1[9] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
  int* result_test1 = array_union(test1_array1, 5, test1_array2, 4);
  tests_result &= test_assert("Prueba unión de dos arreglos ordenados sin elementos repetidos", 
                              compare_arrays(result_test1, expected_test1, 9));
  free(result_test1);

  int test2_array1[3] = {3, 2, 1};
  int test2_array2[3] = {2, 3, 4};
  int expected_test2[4] = {1, 2, 3, 4};
  int* result_test2 = array_union(test2_array1, 3, test2_array2, 3);
  tests_result &= test_assert("Prueba unión de dos arreglos con algunos elementos comunes", 
                              compare_arrays(result_test2, expected_test2, 4));
  free(result_test2);

  int test3_array1[3] = {9, 1, 5};
  int test3_array2[4] = {3, 11, 7, 5};
  int expected_test3[6] = {1, 3, 5, 7, 9, 11};
  int* result_test3 = array_union(test3_array1, 3, test3_array2, 4);
  tests_result &= test_assert("Prueba unión con elementos comunes", 
                              compare_arrays(result_test3, expected_test3, 6));
  free(result_test3);

  int test4_array1[0] = {};
  int test4_array2[4] = {1, 2, 3, 4};
  int expected_test4[4] = {1, 2, 3, 4};
  int* result_test4 = array_union(test4_array1, 0, test4_array2, 4);
  tests_result &= test_assert("Prueba unión con un arreglo vacío", 
                              compare_arrays(result_test4, expected_test4, 4));
  free(result_test4);

  int test5_array1[4] = {1, 7, 5, 3};
  int test5_array2[4] = {8, 4, 6, 2};
  int expected_test5[8] = {1, 2, 3, 4, 5, 6, 7, 8};
  int* result_test5 = array_union(test5_array1, 4, test5_array2, 4);
  tests_result &= test_assert("Prueba unión de dos arreglos con longitud igual", 
                              compare_arrays(result_test5, expected_test5, 8));
  free(result_test5);
  
  int test6_array1[0] = {};
  int test6_array2[0] = {};
  int expected_test6[0] = {};
  int* result_test6 = array_union(test6_array1, 0, test6_array2, 0);
  tests_result &= test_assert("Prueba unión con dos arreglos vacíos", 
                              compare_arrays(result_test6, expected_test6, 0));
  free(result_test6);

  return tests_result;
}

int double_int(int a) { return a * 2; }

bool test_matrix_map() {
  bool tests_result = true;

  int m = 3, n = 3;
  
  int **matrix_test1 = malloc(sizeof(int*) * m);
  if(!matrix_test1) return tests_result;
  for (int i = 0; i < m; i++) {
    matrix_test1[i] = malloc(sizeof(int) * n);
    for (int j = 0; j < n; j++) {
      matrix_test1[i][j] = i * n + j;
    }
  }
  
  matrix_map(matrix_test1, m, n, double_int);
  
  bool test_result = true;
  for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
      test_result &= matrix_test1[i][j] == (i * n + j) * 2;
    }
  }
  
  tests_result &= test_assert("Prueba map de matriz duplicando entero", test_result);

  for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
      matrix_test1[i][j] = i * n + j;
    }
  }

  matrix_map(matrix_test1, m, n, NULL);

  for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
      test_result &= matrix_test1[i][j] == (i * n + j);
    }
  }

  tests_result &= test_assert("Prueba map de matriz sin función", test_result);

  for (int i = 0; i < m; i++) {
    free(matrix_test1[i]);
  }
  free(matrix_test1);

  return tests_result;
}

bool test_matrix_equal() {
  bool tests_result = true;

  int matrix1_1[2][2] = {{1, 2}, {3, 4}};
  int matrix2_1[2][2] = {{5, 6}, {7, 8}};
  int matrix2_2[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
  int matrix3_1[2][3] = {{1, 2, 3}, {4, 5, 6}};
  int matrix4_1[1][4] = {{10, 20, 30, 40}};
  
  int **matrix1 = malloc(2 * sizeof(int *));
  int **matrix2 = malloc(2 * sizeof(int *));
  int **matrix3 = malloc(2 * sizeof(int *));
  int **matrix4 = malloc(1 * sizeof(int *));

  matrix1[0] = (int *) malloc(sizeof(int) * 2);
  matrix1[1] = (int *) malloc(sizeof(int) * 2);
  matrix2[0] = (int *) malloc(sizeof(int) * 2);
  matrix2[1] = (int *) malloc(sizeof(int) * 2);
  matrix3[0] = (int *) malloc(sizeof(int) * 3);
  matrix3[1] = (int *) malloc(sizeof(int) * 3);
  matrix4[0] = (int *) malloc(sizeof(int) * 4);

  for (int i = 0; i < 2; i++) {
    matrix1[0][i] = matrix1_1[0][i];
    matrix1[1][i] = matrix1_1[1][i];
    matrix2[0][i] = matrix2_1[0][i];
    matrix2[1][i] = matrix2_1[1][i];
  }

  for (int i = 0; i < 3; i++) {
    matrix3[0][i] = matrix3_1[0][i];
    matrix3[1][i] = matrix3_1[1][i];
  }

  for (int i = 0; i < 4; i++) {
    matrix4[0][i] = matrix4_1[0][i];
  }

  tests_result &= test_assert("Matrices 2x2 iguales", matrix_equal((const Matriz)matrix1, 2, 2, (const Matriz)matrix1, 2, 2));
  tests_result &= test_assert("Matrices 2x2 diferentes", !matrix_equal((const Matriz)matrix1, 2, 2, (const Matriz)matrix2, 2, 2));
  tests_result &= test_assert("Matrices 2x2 nulas", matrix_equal(NULL, 2, 2, NULL, 2, 2));
  tests_result &= test_assert("Matrices con filas/columnas distintas", !matrix_equal((const Matriz)matrix1, 2, 2, (const Matriz)matrix2, 2, 3));
  tests_result &= test_assert("Matrices 3x3 diferentes", !matrix_equal((const Matriz)matrix1, 2, 2, (const Matriz)matrix2_2, 3, 3));
  tests_result &= test_assert("Matrices 2x3 iguales", matrix_equal((const Matriz)matrix3, 2, 3, (const Matriz)matrix3, 2, 3));
  tests_result &= test_assert("Matrices 1x4 iguales", matrix_equal((const Matriz)matrix4, 1, 4, (const Matriz)matrix4, 1, 4));
  tests_result &= test_assert("Matrices con un NULL", !matrix_equal((const Matriz)matrix1, 2, 2, NULL, 2, 2));
  tests_result &= test_assert("Matrices NULL y NULL", matrix_equal(NULL, 2, 2, NULL, 2, 2));

  for (int i = 0; i < 2; i++) {
    free(matrix1[i]);
    free(matrix2[i]);
  }
  free(matrix1);
  free(matrix2);
  for (int i = 0; i < 2; i++) {
    free(matrix3[i]);
  }
  free(matrix3);
  free(matrix4[0]);
  free(matrix4);

  return tests_result;
}

bool test_copy_matrix() {
  bool tests_result = true;
  
  int m = 6, n = 6;
  int **matrix_test1 = malloc(sizeof(int*) * m);
  
  for (int i = 0; i < m; i++) {
    matrix_test1[i] = malloc(sizeof(int) * n);
    for (int j = 0; j < n; j++) {
      matrix_test1[i][j] = i * n + j;
    }
  }
  
  int **matrix_copy = copy_matrix((const Matriz)matrix_test1, m, n);
  
  bool test_result = true;
  for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
      test_result &= matrix_test1[i][j] == matrix_copy[i][j];
      matrix_copy[i][j] = matrix_copy[i][j] * 2;
      test_result &= matrix_copy[i][j] == matrix_test1[i][j] * 2;
    }
  }

  tests_result &= test_assert("Prueba copiar matriz", test_result);
  
  // Copiar NULL
  test_result = (copy_matrix(NULL, m, n) == NULL);
  tests_result &= test_assert("Prueba copiar matriz nula", test_result);

  // Libera la memoria
  for (int i = 0; i < m; i++) {
    free(matrix_test1[i]);
    free(matrix_copy[i]);
  }
  free(matrix_test1);
  free(matrix_copy);

  return tests_result;
}

bool test_copy_array_of_matrices() {
  bool tests_result = true;

  int array_amount = 4;

  int matrix1[2][2] = {{1, 2}, {3, 4}};
  int matrix2[3][3] = {{5, 6, 7}, {8, 9, 10}, {11, 12, 13}};
  int matrix3[2][3] = {{14, 15, 16}, {17, 18, 19}};
  int matrix4[1][4] = {{20, 21, 22, 23}};

  Matriz* array_of_matrices = malloc(sizeof(int*) * 4);

  array_of_matrices[0] = (Matriz) malloc(sizeof(int*) * 2);
  array_of_matrices[1] = (Matriz) malloc(sizeof(int*) * 3);
  array_of_matrices[2] = (Matriz) malloc(sizeof(int*) * 2);
  array_of_matrices[3] = (Matriz) malloc(sizeof(int*) * 1);

  for (int i = 0; i < 2; i++) {
    array_of_matrices[0][i] = (int* ) malloc(sizeof(int) * 2);
    for (int j = 0; j < 2; j++) {
      array_of_matrices[0][i][j] = matrix1[i][j];
    }
  }

  for (int i = 0; i < 3; i++) {
    array_of_matrices[1][i] = (int* ) malloc(sizeof(int) * 3);
    for (int j = 0; j < 3; j++) {
      array_of_matrices[1][i][j] = matrix2[i][j];
    }
  }

  for (int i = 0; i < 2; i++) {
    array_of_matrices[2][i] = (int *) malloc(sizeof(int) * 3);
    for (int j = 0; j < 3; j++) {
      array_of_matrices[2][i][j] = matrix3[i][j];
    }
  }

  for (int i = 0; i < 1; i++) {
    array_of_matrices[3][i] = (int *) malloc(sizeof(int) * 4);
    for (int j = 0; j < 4; j++) {
      array_of_matrices[3][i][j] = matrix4[i][j];
    }
  }

  int **matrix_dimensions = malloc(sizeof(int*) * array_amount);
  for (int i = 0; i < array_amount; i++) {
    matrix_dimensions[i] = malloc(sizeof(int) * 2);
  }

  matrix_dimensions[0][0] = 2;
  matrix_dimensions[0][1] = 2;
  matrix_dimensions[1][0] = 3;
  matrix_dimensions[1][1] = 3;
  matrix_dimensions[2][0] = 2;
  matrix_dimensions[2][1] = 3;
  matrix_dimensions[3][0] = 1;
  matrix_dimensions[3][1] = 4;

  int ***copied_matrices = copy_array_of_matrices((const Matriz*) array_of_matrices, (const Matriz)matrix_dimensions, array_amount);

  bool test_result = true;

  for (int i = 0; i < array_amount; i++) {
    for (int j = 0; j < matrix_dimensions[i][0]; j++) {
      for (int k = 0; k < matrix_dimensions[i][1]; k++) {
        test_result &= array_of_matrices[i][j][k] == copied_matrices[i][j][k];
        copied_matrices[i][j][k] *= 2;
        test_result &= copied_matrices[i][j][k] == array_of_matrices[i][j][k] * 2;
      }
    }
  }

  tests_result &= test_assert("Prueba copiar arreglo de matrices con diferentes tamaños", test_result);

  test_result = (copy_array_of_matrices(NULL, (const Matriz) matrix_dimensions, array_amount) == NULL);
  tests_result &= test_assert("Prueba copiar arreglo de matrices nulo", test_result);

  for (int i = 0; i < array_amount; i++) {
    for (int j = 0; j < matrix_dimensions[i][0]; j++) {
      free(array_of_matrices[i][j]);
      free(copied_matrices[i][j]);
    }
    free(array_of_matrices[i]);
    free(copied_matrices[i]);
    free(matrix_dimensions[i]);
  }

  free(array_of_matrices);
  free(copied_matrices);
  free(matrix_dimensions);

  return tests_result;
}

bool test_free_array_of_matrices() {
  int array_amount = 2;
  int ***array_of_matrices = malloc(2 * sizeof(int*));

  int matrix1[2][2] = {{1, 2}, {3, 4}};
  int matrix2[2][2] = {{5, 6}, {7, 8}};
  
  array_of_matrices[0] = (int **) malloc(sizeof(int*) * 2);
  array_of_matrices[1] = (int **) malloc(sizeof(int*) * 2);

  for (int i = 0; i < 2; i++) {
    array_of_matrices[0][i] = (int*) malloc(sizeof(int) * 2);
    array_of_matrices[1][i] = (int*) malloc(sizeof(int) * 2);
    for (int j = 0; j < 2; j++) {
      array_of_matrices[0][i][j] = matrix1[i][j];
      array_of_matrices[1][i][j] = matrix2[i][j];
    }
  }

  int **matrix_dimensions = malloc(sizeof(int*) * array_amount);
  for (int i = 0; i < array_amount; i++) {
    matrix_dimensions[i] = malloc(sizeof(int) * 2);
    matrix_dimensions[i][0] = 2;
    matrix_dimensions[i][1] = 2;
  }

  free_array_of_matrices(array_of_matrices, matrix_dimensions, array_amount);

  return true;
}

int main(void) {
  int return_code = 0;
  return_code += !test_are_friends_numbers();
  return_code += !test_calculate_time_in_seconds();
  return_code += !test_swap();
  return_code += !test_array_min_index();
  return_code += !test_array_union();
  return_code += !test_array_copy();
  return_code += !test_selection_sort();
  return_code += !test_matrix_map();
  return_code += !test_matrix_equal();
  return_code += !test_copy_matrix();
  return_code += !test_copy_array_of_matrices();
  return_code += !test_free_array_of_matrices();
  if (return_code == 0) {
    printf("Todo ok!\n");
  } else {
    printf("Error code is %d\n", return_code);
  }

  return return_code;
}
