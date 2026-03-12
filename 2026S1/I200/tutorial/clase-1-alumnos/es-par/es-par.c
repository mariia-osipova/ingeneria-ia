#include <stdio.h>

// Una que determina si un número es par

int esPar(int numero) {
    return 0;
}

int main() {
    int numero;
    printf("Ingrese un numero: ");
    scanf("%d", &numero);

    if (esPar(numero)) {
        printf("%d es un numero par.\n", numero);
    } else {
        printf("%d es un numero impar.\n", numero);
    }

    return 0;
}