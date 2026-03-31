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

// Dadas dos listas ordenadas ascendientemente, se pide devolver la cabeza de una nueva lista
// que contiene todos los elementos de ambas ordenada ascendientemente.
node_t* combinar_listas(node_t* head1, node_t* head2) {
   
}

int main(){
	
	printf("=== PRUEBA 1: Listas básicas con elementos intercalados ===\n");
	node_t* node1 = (node_t*) malloc(sizeof(node_t));
	node_t* node2 = (node_t*) malloc(sizeof(node_t));
	node_t* node3 = (node_t*) malloc(sizeof(node_t));

	node1->val = 3;
	node1->sig = node2;
	
	node2->val = 5;
	node2->sig = node3;
	
	node3->val = 10;
	node3->sig = NULL;

	node_t* node4 = (node_t*) malloc(sizeof(node_t));
	node_t* node5 = (node_t*) malloc(sizeof(node_t));
	node_t* node6 = (node_t*) malloc(sizeof(node_t));

	node4->val = 6;
	node4->sig = node5;
	
	node5->val = 20;
	node5->sig = node6;
	
	node6->val = 30;
	node6->sig = NULL;
	
	printf("Lista 1: ");
	imprimir_lista(node1);
	printf("Lista 2: ");
	imprimir_lista(node4);

	node_t* combinadas = combinar_listas(node1, node4);
	printf("Resultado esperado: 3 -> 5 -> 6 -> 10 -> 20 -> 30 -> NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(combinadas);

	// Liberar memoria de la primera prueba (los nodos son los mismos que los originales)
	node_t* current = combinadas;
	while(current) {
		node_t* temp = current;
		current = current->sig;
		free(temp);
	}

	printf("\n=== PRUEBA 2: Una lista vacía ===\n");
	node_t* lista_vacia = NULL;
	node_t* lista_no_vacia1 = (node_t*) malloc(sizeof(node_t));
	node_t* lista_no_vacia2 = (node_t*) malloc(sizeof(node_t));
	
	lista_no_vacia1->val = 1;
	lista_no_vacia1->sig = lista_no_vacia2;
	lista_no_vacia2->val = 3;
	lista_no_vacia2->sig = NULL;

	printf("Lista vacía: ");
	imprimir_lista(lista_vacia);
	printf("Lista con datos: ");
	imprimir_lista(lista_no_vacia1);

	node_t* resultado2 = combinar_listas(lista_vacia, lista_no_vacia1);
	printf("Resultado esperado: 1 -> 3 -> NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(resultado2);

	// Liberar memoria (los nodos son los mismos que los originales)
	current = resultado2;
	while(current) {
		node_t* temp = current;
		current = current->sig;
		free(temp);
	}

	printf("\n=== PRUEBA 3: Ambas listas vacías ===\n");
	node_t* vacia1 = NULL;
	node_t* vacia2 = NULL;
	
	printf("Lista 1 vacía: ");
	imprimir_lista(vacia1);
	printf("Lista 2 vacía: ");
	imprimir_lista(vacia2);

	node_t* resultado3 = combinar_listas(vacia1, vacia2);
	printf("Resultado esperado: NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(resultado3);

	printf("\n=== PRUEBA 4: Un solo elemento cada una ===\n");
	node_t* single1 = (node_t*) malloc(sizeof(node_t));
	node_t* single2 = (node_t*) malloc(sizeof(node_t));
	
	single1->val = 2;
	single1->sig = NULL;
	single2->val = 4;
	single2->sig = NULL;

	printf("Lista 1: ");
	imprimir_lista(single1);
	printf("Lista 2: ");
	imprimir_lista(single2);

	node_t* resultado4 = combinar_listas(single1, single2);
	printf("Resultado esperado: 2 -> 4 -> NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(resultado4);

	// Liberar memoria (los nodos son los mismos que los originales)
	current = resultado4;
	while(current) {
		node_t* temp = current;
		current = current->sig;
		free(temp);
	}

	printf("\n=== PRUEBA 5: Todos los elementos de lista1 menores que lista2 ===\n");
	node_t* menor1 = (node_t*) malloc(sizeof(node_t));
	node_t* menor2 = (node_t*) malloc(sizeof(node_t));
	node_t* mayor1 = (node_t*) malloc(sizeof(node_t));
	node_t* mayor2 = (node_t*) malloc(sizeof(node_t));

	menor1->val = 1;
	menor1->sig = menor2;
	menor2->val = 2;
	menor2->sig = NULL;

	mayor1->val = 10;
	mayor1->sig = mayor2;
	mayor2->val = 20;
	mayor2->sig = NULL;

	printf("Lista menores: ");
	imprimir_lista(menor1);
	printf("Lista mayores: ");
	imprimir_lista(mayor1);

	node_t* resultado5 = combinar_listas(menor1, mayor1);
	printf("Resultado esperado: 1 -> 2 -> 10 -> 20 -> NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(resultado5);

	// Liberar memoria (los nodos son los mismos que los originales)
	current = resultado5;
	while(current) {
		node_t* temp = current;
		current = current->sig;
		free(temp);
	}

	printf("\n=== PRUEBA 6: Listas de diferentes tamaños ===\n");
	node_t* corta1 = (node_t*) malloc(sizeof(node_t));
	node_t* larga1 = (node_t*) malloc(sizeof(node_t));
	node_t* larga2 = (node_t*) malloc(sizeof(node_t));
	node_t* larga3 = (node_t*) malloc(sizeof(node_t));
	node_t* larga4 = (node_t*) malloc(sizeof(node_t));

	corta1->val = 5;
	corta1->sig = NULL;

	larga1->val = 1;
	larga1->sig = larga2;
	larga2->val = 3;
	larga2->sig = larga3;
	larga3->val = 7;
	larga3->sig = larga4;
	larga4->val = 9;
	larga4->sig = NULL;

	printf("Lista corta: ");
	imprimir_lista(corta1);
	printf("Lista larga: ");
	imprimir_lista(larga1);

	node_t* resultado6 = combinar_listas(corta1, larga1);
	printf("Resultado esperado: 1 -> 3 -> 5 -> 7 -> 9 -> NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(resultado6);

	// Liberar memoria (los nodos son los mismos que los originales)
	current = resultado6;
	while(current) {
		node_t* temp = current;
		current = current->sig;
		free(temp);
	}

	printf("\n=== PRUEBA 7: Elementos duplicados ===\n");
	node_t* dup1_1 = (node_t*) malloc(sizeof(node_t));
	node_t* dup1_2 = (node_t*) malloc(sizeof(node_t));
	node_t* dup2_1 = (node_t*) malloc(sizeof(node_t));
	node_t* dup2_2 = (node_t*) malloc(sizeof(node_t));

	dup1_1->val = 2;
	dup1_1->sig = dup1_2;
	dup1_2->val = 5;
	dup1_2->sig = NULL;

	dup2_1->val = 2;
	dup2_1->sig = dup2_2;
	dup2_2->val = 5;
	dup2_2->sig = NULL;

	printf("Lista 1: ");
	imprimir_lista(dup1_1);
	printf("Lista 2: ");
	imprimir_lista(dup2_1);

	node_t* resultado7 = combinar_listas(dup1_1, dup2_1);
	printf("Resultado esperado: 2 -> 2 -> 5 -> 5 -> NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(resultado7);

	// Liberar memoria (los nodos son los mismos que los originales)
	current = resultado7;
	while(current) {
		node_t* temp = current;
		current = current->sig;
		free(temp);
	}

	printf("\n¡Todas las pruebas completadas!\n");
}
