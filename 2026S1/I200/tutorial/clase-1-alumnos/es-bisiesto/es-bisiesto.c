#include <stdio.h>
#include <stdbool.h>

bool esBisiesto(int anio) {
    if (anio % 4 != 0) return false;
    else if (anio % 100 == 0 && anio % 400 != 0) return false;
    else return true;
}

void realizarPrueba(int anio, bool esperado) {
    int resultado = esBisiesto(anio);
    
    printf("Prueba para el año %d: ", anio);
    
    if (resultado == esperado) {
        printf("Aprobada\n");
    } else {
        printf("Falla la prueba\n");
    }
}

int main() {
    realizarPrueba(2000, true); 
    realizarPrueba(2021, false);  
    realizarPrueba(2100, false);  
    realizarPrueba(2400, true); 
    realizarPrueba(2024, true); 

    return 0;
}