#include <stdio.h>
#include <stdbool.h>

typedef struct Node{
    int x;
    struct Node *sig;
}Node;

Node crearNodo(int x){
  struct Node nodo;
  nodo.x = x;
  return nodo;
}

void conectar(Node *a, Node *b){
  a->sig = b;
}

void saltar(Node *currentNode){
  currentNode = currentNode->sig;
}

bool esCircular_1(Node *punteroInicial){
  Node *first = punteroInicial;
  Node *actual = punteroInicial->sig;
  while(actual != punteroInicial){
    actual++;
    if (actual->sig == NULL) return false;
  }
  return true;
}

bool esCircular_2(Node *punteroInicial){
  Node *slowly = punteroInicial;
  Node *speedy = punteroInicial->sig;
  while(slowly != speedy && speedy->sig != slowly){
    slowly ++;
    speedy = speedy + 2;
    if (speedy == NULL || slowly == NULL) return false; //slowly por las dudas
  }
  return true;
}

int main() {

}