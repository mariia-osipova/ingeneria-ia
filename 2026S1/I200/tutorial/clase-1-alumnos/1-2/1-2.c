#include <stdio.h>

// Escribir la función que dado n P N devuelve la suma de todos los números
// impares menores que n.
int sumaImparesMenoresQueN(int n) {
  	int suma = 0;
   	for (int i = 0; i < n; i ++){
       if (i % 2 != 0) suma = suma+i;
    }
    return suma;
}


int main() {
    int n;
    printf("Ingrese un numero: ");
    scanf("%d", &n);

    int resultado = sumaImparesMenoresQueN(n);
    printf("La suma de los numeros impares menores que %d es: %d\n", n, resultado);

    return 0;
}
