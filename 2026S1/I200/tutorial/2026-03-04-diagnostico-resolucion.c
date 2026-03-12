#include <stdio.h>

/* =========================================================
   1) Función que recibe 4 enteros y retorna el mayor valor
   ========================================================= */
int Mayor(int a, int b, int c, int d) {
    int max = a;
    if (b > max) max = b;
    if (c > max) max = c;
    if (d > max) max = d;
    return max;
}

/* =========================================================
   2) Función recursiva para la serie SerieX(i)
      SerieX(0) = 3
      SerieX(1) = 7
      SerieX(2) = 2
      SerieX(i) = SerieX(i-2) - 2*SerieX(i-1) + 4*SerieX(i-3)  si i > 2
   ========================================================= */
int SerieX(int i) {
    if (i == 0) return 3;
    if (i == 1) return 7;
    if (i == 2) return 2;
    return SerieX(i-2) - 2 * SerieX(i-1) + 4 * SerieX(i-3);
}

/* --- Opción B: Bottom-up iterativo (más eficiente en stack) --- */
int SerieX_dp(int i) {
    if (i == 0) return 3;
    if (i == 1) return 7;
    if (i == 2) return 2;

    int dp[i + 1];
    dp[0] = 3; dp[1] = 7; dp[2] = 2;

    for (int k = 3; k <= i; k++)
        dp[k] = dp[k-2] - 2 * dp[k-1] + 4 * dp[k-3];

    return dp[i];
}

/* =========================================================
   3) Función que analiza una lista de dígitos y encuentra
      la sublista de dígitos iguales más larga.
      Retorna por punteros:
        - inicio:  posición de inicio de la cadena más larga
        - largo:   longitud de la cadena más larga
        - digito:  dígito que se repite
   ========================================================= */
void analizar(int lista_p[], int n, int *inicio, int *largo, int *digito) {
    *inicio = 0;
    *largo  = 1;
    *digito = lista_p[0];

    int cur_inicio = 0;
    int cur_largo  = 1;

    for (int i = 1; i < n; i++) {
        if (lista_p[i] == lista_p[i-1]) {
            cur_largo++;
        } else {
            cur_inicio = i;
            cur_largo  = 1;
        }

        if (cur_largo > *largo) {
            *inicio = cur_inicio;
            *largo  = cur_largo;
            *digito = lista_p[i];
        }
    }
}

/* =========================================================
   Main - pruebas
   ========================================================= */
int main() {
    /* --- Ejercicio 1 --- */
    printf("=== Mayor ===\n");
    printf("Mayor(3, 7, 2, 5) = %d\n\n", Mayor(3, 7, 2, 5)); // esperado: 7

    /* --- Ejercicio 2 --- */
    printf("=== SerieX ===\n");
    for (int i = 0; i <= 6; i++)
        printf("SerieX(%d) = %d\n", i, SerieX(i));
    printf("\n");

    /* --- Ejercicio 3 --- */
    printf("=== Analizar ===\n");
    int lista[] = {1, 2, 3, 3, 3, 4, 1, 1, 1, 1, 7, 4};
    int n = sizeof(lista) / sizeof(lista[0]);

    int inicio, largo, digito;
    analizar(lista, n, &inicio, &largo, &digito);

    printf("Inicio : %d\n", inicio);  // esperado: 6
    printf("Largo  : %d\n", largo);   // esperado: 4
    printf("Digito : %d\n", digito);  // esperado: 1

    return 0;
}