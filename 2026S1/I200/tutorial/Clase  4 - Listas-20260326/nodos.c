#include <stdlib.h>
#include <stdio.h>

typedef struct Nodo {
	int val; 
	struct Nodo* sig;
} node_t;

void imprimir_lista(node_t* head) {
	while(head) {
		printf("%d -> ", head->val);
		head = head->sig;
	}
	printf("NULL\n");
}


// Devuelve el tamaño de la lista.
int size(node_t* head) {
	// TODO
}

// Agrega un elemento al final y devuelve el puntero a la cabeza.
node_t* agregarAlFinal(node_t* head, int val) {
//	node_t *aux = head;

	node_t *nuevo = malloc(sizeof(node_t));
    if (nuevo == NULL) return NULL;

	nuevo->val = val;
	nuevo->sig = NULL;

    if (head == NULL) return nuevo;

	node_t* actual = head;

    while(actual -> sig != NULL){
      actual = actual -> sig;
    }

	actual->sig = nuevo;
    return head;
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
	
	printf("Cantidad de elementos: %d (esperado: 3)\n", size(node1));
	printf("Lista: ");
	imprimir_lista(node1);

	printf("\n=== TEST 2: Agregar elemento al final ===\n");
	node_t* head = agregarAlFinal(node1, 10);
	
	printf("Cantidad de elementos: %d (esperado: 4)\n", size(head));
	printf("Lista: ");
	imprimir_lista(head);

	printf("\n=== TEST 3: Agregar otro elemento ===\n");
	head = agregarAlFinal(head, 20);
	printf("Cantidad de elementos: %d (esperado: 5)\n", size(head));
	printf("Lista: ");
	imprimir_lista(head);

	printf("\n=== TEST 4: Lista vacía ===\n");
	node_t* empty_list = NULL;
	printf("Cantidad de elementos en lista vacía: %d (esperado: 0)\n", size(empty_list));
	printf("Lista vacía: ");
	imprimir_lista(empty_list);

	printf("\n=== TEST 5: Agregar a lista vacía ===\n");
	node_t* new_head = agregarAlFinal(empty_list, 100);
	printf("Cantidad de elementos: %d (esperado: 1)\n", size(new_head));
	printf("Lista: ");
	imprimir_lista(new_head);

	printf("\n=== TEST 6: Un solo elemento ===\n");
	node_t* single = (node_t*) malloc(sizeof(node_t));
	single->val = 42;
	single->sig = NULL;
	printf("Cantidad de elementos: %d (esperado: 1)\n", size(single));
	printf("Lista: ");
	imprimir_lista(single);

	printf("\n=== TEST 7: Agregar múltiples elementos consecutivos ===\n");
	node_t* multi = agregarAlFinal(single, 50);
	multi = agregarAlFinal(multi, 60);
	multi = agregarAlFinal(multi, 70);
	printf("Cantidad de elementos: %d (esperado: 4)\n", size(multi));
	printf("Lista: ");
	imprimir_lista(multi);

	printf("\n=== Liberando memoria ===\n");
	// Liberar la lista original de prueba (nota: deberíamos considerar los nuevos nodos agregados)
	// Por ahora, solo liberamos los 3 nodos originales; en un caso real,
	// deberías recorrer y liberar toda la lista modificada
	free(node1);
	free(node2);
	free(node3);
	
	// Liberar el nodo de la prueba de un solo elemento
	free(single);
	
	// Liberar new_head si fue creado
	if (new_head) {
		free(new_head);
	}
	
	printf("Nota: En una implementación completa, deberías liberar toda la lista modificada\n");
}


