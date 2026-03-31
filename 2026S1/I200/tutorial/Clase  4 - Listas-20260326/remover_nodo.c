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


list_t* remove_node(list_t *list, node_t *node) {

	node_t* actual = list->head;

	if (actual == NULL) return NULL;

	// if (node == NULL) return NULL;

	if (node == list->head) {
		list->head = node->sig;
		if (list->size == 1)
		// free(node);
	}



	else if (node == list->tail) {
		node->sig = NULL;
		list->tail->sig = &node;
		list->tail = node;
	}

}

int main(){
	
	printf("=== TEST 1: Remover nodo del medio ===\n");
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

	printf("Lista original: ");
	imprimir_lista(lista);
	printf("Cantidad de elementos: %d (esperado: 3)\n", lista->size);
	
	lista = remove_node(lista, node2);
	printf("Después de remover nodo con valor 2:\n");
	printf("Lista: ");
	imprimir_lista(lista);
	printf("Cantidad de elementos: %d (esperado: 2)\n", lista->size);

	printf("\n=== TEST 2: Remover primer nodo (head) ===\n");
	node_t* nodeA = (node_t*) malloc(sizeof(node_t));
	node_t* nodeB = (node_t*) malloc(sizeof(node_t));
	node_t* nodeC = (node_t*) malloc(sizeof(node_t));

	nodeA->val = 10;
	nodeA->sig = nodeB;
	nodeB->val = 20;
	nodeB->sig = nodeC;
	nodeC->val = 30;
	nodeC->sig = NULL;

	list_t* lista2 = (list_t*) malloc(sizeof(list_t));
	lista2->head = nodeA;
	lista2->tail = nodeC;
	lista2->size = 3;

	printf("Lista original: ");
	imprimir_lista(lista2);
	
	lista2 = remove_node(lista2, nodeA);
	printf("Después de remover primer nodo (head):\n");
	printf("Lista: ");
	imprimir_lista(lista2);
	printf("Cantidad de elementos: %d (esperado: 2)\n", lista2->size);

	printf("\n=== TEST 3: Remover último nodo (tail) ===\n");
	node_t* nodeX = (node_t*) malloc(sizeof(node_t));
	node_t* nodeY = (node_t*) malloc(sizeof(node_t));
	node_t* nodeZ = (node_t*) malloc(sizeof(node_t));

	nodeX->val = 100;
	nodeX->sig = nodeY;
	nodeY->val = 200;
	nodeY->sig = nodeZ;
	nodeZ->val = 300;
	nodeZ->sig = NULL;

	list_t* lista3 = (list_t*) malloc(sizeof(list_t));
	lista3->head = nodeX;
	lista3->tail = nodeZ;
	lista3->size = 3;

	printf("Lista original: ");
	imprimir_lista(lista3);
	
	lista3 = remove_node(lista3, nodeZ);
	printf("Después de remover último nodo (tail):\n");
	printf("Lista: ");
	imprimir_lista(lista3);
	printf("Cantidad de elementos: %d (esperado: 2)\n", lista3->size);
	if (lista3->tail) {
		printf("Nuevo tail tiene valor: %d (esperado: 200)\n", lista3->tail->val);
	}

	printf("\n=== TEST 4: Remover de lista con un solo elemento ===\n");
	node_t* nodo_unico = (node_t*) malloc(sizeof(node_t));
	nodo_unico->val = 42;
	nodo_unico->sig = NULL;

	list_t* lista_unica = (list_t*) malloc(sizeof(list_t));
	lista_unica->head = nodo_unico;
	lista_unica->tail = nodo_unico;
	lista_unica->size = 1;

	printf("Lista original: ");
	imprimir_lista(lista_unica);
	
	lista_unica = remove_node(lista_unica, nodo_unico);
	printf("Después de remover único elemento:\n");
	printf("Lista: ");
	imprimir_lista(lista_unica);
	printf("Cantidad de elementos: %d (esperado: 0)\n", lista_unica->size);

	printf("\n=== TEST 5: Intentar remover de lista vacía ===\n");
	list_t* lista_vacia = (list_t*) malloc(sizeof(list_t));
	lista_vacia->head = NULL;
	lista_vacia->tail = NULL;
	lista_vacia->size = 0;

	printf("Lista vacía antes: ");
	imprimir_lista(lista_vacia);
	
	// Intentar remover un nodo NULL
	lista_vacia = remove_node(lista_vacia, NULL);
	printf("Después de intentar remover de lista vacía:\n");
	printf("Lista: ");
	imprimir_lista(lista_vacia);
	printf("Cantidad de elementos: %d (esperado: 0)\n", lista_vacia->size);

	printf("\n=== TEST 6: Remover múltiples nodos consecutivamente ===\n");
	node_t* multi1 = (node_t*) malloc(sizeof(node_t));
	node_t* multi2 = (node_t*) malloc(sizeof(node_t));
	node_t* multi3 = (node_t*) malloc(sizeof(node_t));
	node_t* multi4 = (node_t*) malloc(sizeof(node_t));

	multi1->val = 5;
	multi1->sig = multi2;
	multi2->val = 15;
	multi2->sig = multi3;
	multi3->val = 25;
	multi3->sig = multi4;
	multi4->val = 35;
	multi4->sig = NULL;

	list_t* lista_multi = (list_t*) malloc(sizeof(list_t));
	lista_multi->head = multi1;
	lista_multi->tail = multi4;
	lista_multi->size = 4;

	printf("Lista original: ");
	imprimir_lista(lista_multi);
	
	// Remover el segundo nodo
	lista_multi = remove_node(lista_multi, multi2);
	printf("Después de remover nodo con valor 15: ");
	imprimir_lista(lista_multi);
	printf("Cantidad: %d (esperado: 3)\n", lista_multi->size);
	
	// Remover el último nodo
	lista_multi = remove_node(lista_multi, multi4);
	printf("Después de remover nodo con valor 35: ");
	imprimir_lista(lista_multi);
	printf("Cantidad: %d (esperado: 2)\n", lista_multi->size);

	printf("\n=== Liberando memoria ===\n");
	// Liberar memoria (nota: en implementación real, remove_node debería liberar el nodo removido)
	free(node1);
	free(node3);
	free(lista);
	
	free(nodeB);
	free(nodeC);
	free(lista2);
	
	free(nodeX);
	free(nodeY);
	free(lista3);
	
	free(lista_unica);
	free(lista_vacia);
	
	free(multi1);
	free(multi3);
	free(lista_multi);
	
	printf("Nota: En una implementación completa, remove_node debería liberar la memoria del nodo removido\n");
}
