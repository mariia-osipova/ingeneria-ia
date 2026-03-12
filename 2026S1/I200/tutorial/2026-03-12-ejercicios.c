#include <stdio.h>
#include <stdlib.h>


// arrayEqual compara dos arrays de enteros y devuelve 1 si son iguales (mismo tamaño y mismos elementos en el mismo orden) o 0 si no lo son.
int arrayEqual(const int* arr1, int size1, const int* arr2, int size2) {
    if (size1 != size2) return 0;
    int i = 0;
    for (i = 0; i < size1; i++) {
        if (arr1[i] != arr2[i]) return 0;
    }
    return 1;
}


// ReverseArray invierte el orden de los elementos en un array dado. No se puede usar otro array auxiliar, debe hacerse in-place.
void reverseArray(int* arr, int size) {
    int i = 0;
    int j = size - 1;
    int temp;
    while (i < j) {
      temp = arr[i];
      arr[i] = arr[j];
      arr[j] = temp;
      i++;
      j--;
    }
}

// searchMaxApp debe devolver el elemento del 1 al 9 que más veces aparece en el array
int searchMaxApp(int* arr, int size){
    int myMatrix[9][2];
    int j = 0;

    for (int i=0; i <= 8; i++) {
      myMatrix[i][1] = 0;
    }


    while (j < 9) {
       myMatrix[j][0] = j+1;
       j ++;
    }

    int k = 0;

    while (k < size) {
      myMatrix[arr[k]-1][1] ++;
      k++;
    }

    int max = 0;
    int num_max = 0;

    for (int i=0; i <= 8; i++) {
      if (myMatrix[i][1] > max) {
        max = myMatrix[i][1];
        num_max = myMatrix[i][0];
      }
    }

    return num_max;
}

// sumDiagMatrix debe devolver la suma de todos los elementos de la diagonal principal de una matriz cuadrada dada. La matriz se representa como un puntero a puntero (int**), junto con el número de filas y columnas.
int sumDiagMatrix(int** matrix, int rows){
    return 0;
    // TODO
}

int main() {

    int arrayEstatico1[] = {1, 2, 3, 4, 5};
    int sizeEstatico1 = sizeof(arrayEstatico1) / sizeof(arrayEstatico1[0]);

    int* arrayDinamico1 = (int*)malloc(sizeEstatico1 * sizeof(int));
    if (!arrayDinamico1) {
        perror("Error al asignar memoria");
        return EXIT_FAILURE;
    }
    for (int i = 0; i < sizeEstatico1; i++) {
        arrayDinamico1[i] = arrayEstatico1[i];
    }

    // Caso de prueba 2: Arrays diferentes
    int arrayEstatico2[] = {10, 20, 30};
    int sizeEstatico2 = sizeof(arrayEstatico2) / sizeof(arrayEstatico2[0]);

    int* arrayDinamico2 = (int*)malloc(sizeEstatico2 * sizeof(int));
    if (!arrayDinamico2) {
        perror("Error al asignar memoria");
        free(arrayDinamico1);
        return EXIT_FAILURE;
    }
    for (int i = 0; i < sizeEstatico2; i++) {
        arrayDinamico2[i] = arrayEstatico2[i] + 1;
    }

    printf("=== Tests arrayEqual ===\n");

    // Test 1: arrays iguales
    if (arrayEqual(arrayEstatico1, sizeEstatico1, arrayDinamico1, sizeEstatico1)) {
        printf("Test 1 (iguales):    OK\n");
    } else {
        printf("Test 1 (iguales):    FAIL\n");
    }

    // Test 2: arrays diferentes
    if (!arrayEqual(arrayEstatico2, sizeEstatico2, arrayDinamico2, sizeEstatico2)) {
        printf("Test 2 (diferentes): OK\n");
    } else {
        printf("Test 2 (diferentes): FAIL\n");
    }

    // Test 3: distinto tamaño
    int arrA[] = {1, 2, 3};
    int arrB[] = {1, 2};
    if (!arrayEqual(arrA, 3, arrB, 2)) {
        printf("Test 3 (dist. tamaño): OK\n");
    } else {
        printf("Test 3 (dist. tamaño): FAIL\n");
    }

    free(arrayDinamico1);
    free(arrayDinamico2);

    // -------------------------
    printf("\n=== Tests reverseArray ===\n");

    // Test 4: invertir array impar
    int rev1[] = {1, 2, 3, 4, 5};
    int rev1Esp[] = {5, 4, 3, 2, 1};
    reverseArray(rev1, 5);
    if (arrayEqual(rev1, 5, rev1Esp, 5)) {
        printf("Test 4 (impar):  OK\n");
    } else {
        printf("Test 4 (impar):  FAIL\n");
    }

    // Test 5: invertir array par
    int rev2[] = {10, 20, 30, 40};
    int rev2Esp[] = {40, 30, 20, 10};
    reverseArray(rev2, 4);
    if (arrayEqual(rev2, 4, rev2Esp, 4)) {
        printf("Test 5 (par):    OK\n");
    } else {
        printf("Test 5 (par):    FAIL\n");
    }

    // Test 6: array de un elemento
    int rev3[] = {7};
    int rev3Esp[] = {7};
    reverseArray(rev3, 1);
    if (arrayEqual(rev3, 1, rev3Esp, 1)) {
        printf("Test 6 (1 elem): OK\n");
    } else {
        printf("Test 6 (1 elem): FAIL\n");
    }

    // -------------------------
    printf("\n=== Tests searchMaxApp ===\n");

    // Test 7: el 3 aparece más veces
    int app1[] = {1, 3, 2, 3, 3, 5, 2};
    int res7 = searchMaxApp(app1, 7);
    if (res7 == 3) {
        printf("Test 7 (max app = 3): OK\n");
    } else {
        printf("Test 7 (max app = 3): FAIL (obtenido %d)\n", res7);
    }

    // Test 8: todos iguales
    int app2[] = {5, 5, 5, 5};
    int res8 = searchMaxApp(app2, 4);
    if (res8 == 5) {
        printf("Test 8 (todos iguales = 5): OK\n");
    } else {
        printf("Test 8 (todos iguales = 5): FAIL (obtenido %d)\n", res8);
    }

    // Test 9: un solo elemento
    int app3[] = {7};
    int res9 = searchMaxApp(app3, 1);
    if (res9 == 7) {
        printf("Test 9 (un elem = 7): OK\n");
    } else {
        printf("Test 9 (un elem = 7): FAIL (obtenido %d)\n", res9);
    }

    // -------------------------
    printf("\n=== Tests sumDiagMatrix ===\n");

    // Test 10: matriz 3x3
    int r0[] = {1, 2, 3};
    int r1[] = {4, 5, 6};
    int r2[] = {7, 8, 9};
    int* mat3x3[] = {r0, r1, r2};
    int res10 = sumDiagMatrix((int**)mat3x3, 3);
    if (res10 == 15) {  // 1+5+9
        printf("Test 10 (3x3, diag=15): OK\n");
    } else {
        printf("Test 10 (3x3, diag=15): FAIL (obtenido %d)\n", res10);
    }

    // Test 11: matriz 2x2
    int s0[] = {4, 7};
    int s1[] = {2, 3};
    int* mat2x2[] = {s0, s1};
    int res11 = sumDiagMatrix((int**)mat2x2, 2);
    if (res11 == 7) {  // 4+3
        printf("Test 11 (2x2, diag=7): OK\n");
    } else {
        printf("Test 11 (2x2, diag=7): FAIL (obtenido %d)\n", res11);
    }

    // Test 12: matriz 1x1
    int t0[] = {42};
    int* mat1x1[] = {t0};
    int res12 = sumDiagMatrix((int**)mat1x1, 1);
    if (res12 == 42) {
        printf("Test 12 (1x1, diag=42): OK\n");
    } else {
        printf("Test 12 (1x1, diag=42): FAIL (obtenido %d)\n", res12);
    }

    return EXIT_SUCCESS;
}
