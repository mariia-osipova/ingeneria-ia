#include <stdlib.h>
#include <stdio.h>

typedef struct Nodo {
	int val; 
	struct Nodo* sig;
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

// Devuelve el tamaño de la lista.
int size(list_t* list) {
	// TODO
}

// Agrega un elemento al final y devuelve el puntero a la lista
list_t* agregarAlFinal(list_t* list, int val) {
	// TODO
}


int main(){
	
	printf("=== TEST 1: Lista inicial de 3 elementos ===\n");
	node_t* node1 = (node_t*) malloc(sizeof(node_t));
	node_t* node2 = (node_t*) malloc(sizeof(node_t));
	node_t* node3 = (node_t*) malloc(sizeof(node_t));

	node1->val = 1;
	node1->sig = node2;
	
	node2->val = 2;
	node2->sig = node3;
	
	node3->val = 3;
	node3->sig = NULL;

	list_t* lista = (list_t*) malloc(sizeof(list_t));
	lista->head = node1;
	lista->tail = node3;
	lista->size = 3;
	
	printf("Cantidad de elementos: %d (esperado: 3)\n", size(lista));
	printf("Lista: ");
	imprimir_lista(lista);

	printf("\n=== TEST 2: Agregar elemento al final ===\n");
	list_t* l = agregarAlFinal(lista, 10);
	printf("Cantidad de elementos: %d (esperado: 4)\n", size(l));
	printf("Lista: ");
	imprimir_lista(l);

	printf("\n=== TEST 3: Agregar otro elemento ===\n");
	l = agregarAlFinal(l, 20);
	printf("Cantidad de elementos: %d (esperado: 5)\n", size(l));
	printf("Lista: ");
	imprimir_lista(l);

	printf("\n=== TEST 4: Lista vacía ===\n");
	list_t* lista_vacia = (list_t*) malloc(sizeof(list_t));
	lista_vacia->head = NULL;
	lista_vacia->tail = NULL;
	lista_vacia->size = 0;
	printf("Cantidad de elementos en lista vacía: %d (esperado: 0)\n", size(lista_vacia));
	printf("Lista vacía: ");
	imprimir_lista(lista_vacia);

	printf("\n=== TEST 5: Agregar a lista vacía ===\n");
	list_t* nueva_lista = agregarAlFinal(lista_vacia, 100);
	printf("Cantidad de elementos: %d (esperado: 1)\n", size(nueva_lista));
	printf("Lista: ");
	imprimir_lista(nueva_lista);

	printf("\n=== TEST 6: Un solo elemento ===\n");
	node_t* nodo_unico = (node_t*) malloc(sizeof(node_t));
	nodo_unico->val = 42;
	nodo_unico->sig = NULL;
	
	list_t* lista_unica = (list_t*) malloc(sizeof(list_t));
	lista_unica->head = nodo_unico;
	lista_unica->tail = nodo_unico;
	lista_unica->size = 1;
	
	printf("Cantidad de elementos: %d (esperado: 1)\n", size(lista_unica));
	printf("Lista: ");
	imprimir_lista(lista_unica);

	printf("\n=== TEST 7: Agregar múltiples elementos consecutivos ===\n");
	list_t* multi = agregarAlFinal(lista_unica, 50);
	multi = agregarAlFinal(multi, 60);
	multi = agregarAlFinal(multi, 70);
	printf("Cantidad de elementos: %d (esperado: 4)\n", size(multi));
	printf("Lista: ");
	imprimir_lista(multi);

	printf("\n=== TEST 8: Verificar tail después de agregar ===\n");
	// Crear una nueva lista simple para verificar que el tail se actualiza correctamente
	node_t* nodo_test = (node_t*) malloc(sizeof(node_t));
	nodo_test->val = 5;
	nodo_test->sig = NULL;
	
	list_t* lista_test = (list_t*) malloc(sizeof(list_t));
	lista_test->head = nodo_test;
	lista_test->tail = nodo_test;
	lista_test->size = 1;
	
	printf("Lista antes de agregar: ");
	imprimir_lista(lista_test);
	printf("Valor del tail antes: %d\n", lista_test->tail->val);
	
	lista_test = agregarAlFinal(lista_test, 99);
	printf("Lista después de agregar: ");
	imprimir_lista(lista_test);
	printf("Valor del tail después: %d (esperado: 99)\n", lista_test->tail->val);

	printf("\n=== Liberando memoria ===\n");
	// Nota: En una implementación real, deberías recorrer y liberar toda la lista
	// Por simplicidad, liberamos solo los nodos originales
	free(node1);
	free(node2);
	free(node3);
	free(lista);
	free(lista_vacia);
	free(nodo_unico);
	free(lista_unica);
	free(nodo_test);
	free(lista_test);
	
	printf("Nota: En una implementación completa, deberías liberar todos los nodos agregados dinámicamente\n");
}



