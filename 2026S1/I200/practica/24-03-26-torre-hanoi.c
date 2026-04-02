#include <stdio.h>
#include <stdlib.h>

typedef struct Pila {
  int *p;
  unsigned n;
  unsigned reservados;
} Pila;

// |1| -> |2| -> |3|

void init(Pila *pila, int n) {
  pila->p = malloc(sizeof(int) * n);
  pila->reservados = n;
  pila->n = n;
  for (int i = 0; i < n; i++) {
    pila->p[i] = n - i;
  }
}

void move(Pila *origen, Pila *destino) {
  destino->p[destino->n] = origen->p[origen->n - 1];
  destino->n++;
  origen->n--;
}

void hanoi(int n, Pila *inicio, Pila *libre, Pila *final) {
  if (n == 0) return;
  hanoi(n - 1, inicio, final, libre);
  move(inicio, final);
  hanoi(n - 1, libre, inicio, final);
}