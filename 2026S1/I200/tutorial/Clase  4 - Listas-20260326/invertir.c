#include <stdlib.h>
#include <stdio.h>

typedef struct Nodo {
	int val; 
	struct Nodo* sig;
	struct Nodo* prev; // Lista doblemente enlazada
} node_t;

typedef struct Lista {
	node_t* head; 
	node_t* tail;
	int size;
} list_t;

void imprimir_lista(list_t* lista) {
	node_t* tmp = lista->head;
	while(tmp) {
		printf("%d -> ", tmp->val);
		tmp = tmp->sig;
	}
	printf("NULL\n");
}

// Se requiere invertir una lista enlazada y devolver un puntero a la lista invertida.
// Puede implementarse in-place (modificando la lista original y retornando el mismo puntero)
// o con memoria auxiliar (creando una nueva lista sin modificar la original).
list_t* invertir_lista(list_t *list) {
	// TODO
}

int main(){

	printf("=== TEST 1: Lista de 3 elementos (caso básico) ===\n");
	node_t* node1 = (node_t*) malloc(sizeof(node_t));
	node_t* node2 = (node_t*) malloc(sizeof(node_t));
	node_t* node3 = (node_t*) malloc(sizeof(node_t));

	node1->val = 1; node1->prev = NULL; node1->sig = node2;
	node2->val = 2; node2->prev = node1; node2->sig = node3;
	node3->val = 3; node3->prev = node2; node3->sig = NULL;

	list_t* lista = (list_t*) malloc(sizeof(list_t));
	lista->head = node1; lista->tail = node3; lista->size = 3;

	printf("Lista original: "); imprimir_lista(lista);
	list_t* res = invertir_lista(lista);
	printf("Resultado obtenido: "); imprimir_lista(res);
	printf("Resultado esperado: 3 -> 2 -> 1 -> NULL\n");

	printf("\n=== TEST 2: Lista con un solo elemento ===\n");
	node_t* single = (node_t*) malloc(sizeof(node_t));
	single->val = 42; single->prev = NULL; single->sig = NULL;

	list_t* lista_single = (list_t*) malloc(sizeof(list_t));
	lista_single->head = single; lista_single->tail = single; lista_single->size = 1;

	printf("Lista original: "); imprimir_lista(lista_single);
	list_t* res2 = invertir_lista(lista_single);
	printf("Resultado obtenido: "); imprimir_lista(res2);
	printf("Resultado esperado: 42 -> NULL\n");

	printf("\n=== TEST 3: Lista vacía ===\n");
	list_t* lista_vacia = (list_t*) malloc(sizeof(list_t));
	lista_vacia->head = NULL; lista_vacia->tail = NULL; lista_vacia->size = 0;

	printf("Lista original: "); imprimir_lista(lista_vacia);
	list_t* res3 = invertir_lista(lista_vacia);
	printf("Resultado obtenido: "); imprimir_lista(res3);
	printf("Resultado esperado: NULL\n");

	printf("\n=== TEST 4: Lista con 5 elementos ===\n");
	node_t* n1 = (node_t*) malloc(sizeof(node_t));
	node_t* n2 = (node_t*) malloc(sizeof(node_t));
	node_t* n3 = (node_t*) malloc(sizeof(node_t));
	node_t* n4 = (node_t*) malloc(sizeof(node_t));
	node_t* n5 = (node_t*) malloc(sizeof(node_t));

	n1->val = 10; n1->prev = NULL; n1->sig = n2;
	n2->val = 20; n2->prev = n1; n2->sig = n3;
	n3->val = 30; n3->prev = n2; n3->sig = n4;
	n4->val = 40; n4->prev = n3; n4->sig = n5;
	n5->val = 50; n5->prev = n4; n5->sig = NULL;

	list_t* lista_5 = (list_t*) malloc(sizeof(list_t));
	lista_5->head = n1; lista_5->tail = n5; lista_5->size = 5;

	printf("Lista original: "); imprimir_lista(lista_5);
	list_t* res4 = invertir_lista(lista_5);
	printf("Resultado obtenido: "); imprimir_lista(res4);
	printf("Resultado esperado: 50 -> 40 -> 30 -> 20 -> 10 -> NULL\n");

	printf("\n=== TEST 5: Lista con dos elementos ===\n");
	node_t* a = (node_t*) malloc(sizeof(node_t));
	node_t* b = (node_t*) malloc(sizeof(node_t));

	a->val = 100; a->prev = NULL; a->sig = b;
	b->val = 200; b->prev = a; b->sig = NULL;

	list_t* lista_2 = (list_t*) malloc(sizeof(list_t));
	lista_2->head = a; lista_2->tail = b; lista_2->size = 2;

	printf("Lista original: "); imprimir_lista(lista_2);
	list_t* res5 = invertir_lista(lista_2);
	printf("Resultado obtenido: "); imprimir_lista(res5);
	printf("Resultado esperado: 200 -> 100 -> NULL\n");

	printf("\n¡Todas las pruebas completadas!\n");
}
