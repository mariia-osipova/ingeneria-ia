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
	if (!lista || !lista->head) {
		printf("NULL\n");
		return;
	}
	
	node_t* current = lista->head;
	while(current) {
		printf("%d -> ", current->val);
		current = current->sig;
	}
	printf("NULL\n");
}

//Dada una lista, se pide modificarla de forma que no existan dos elementos consecutivos iguales.
// 10 -> 2 -> 2 -> 2 -> 3 -> 5 -> 5 -> 11
// Resultado: 10 -> 2 -> 3 -> 5 -> 11
void remover_consecutivos(list_t* list) {
	// TODO
}

int main(){
	
	printf("=== TEST 1: Lista con duplicados consecutivos múltiples (ejemplo del enunciado) ===\n");
	// Crear lista: 10 -> 2 -> 2 -> 2 -> 3 -> 5 -> 5 -> 11
	node_t* node1 = (node_t*) malloc(sizeof(node_t));
	node_t* node2 = (node_t*) malloc(sizeof(node_t));
	node_t* node3 = (node_t*) malloc(sizeof(node_t));
	node_t* node4 = (node_t*) malloc(sizeof(node_t));
	node_t* node5 = (node_t*) malloc(sizeof(node_t));
	node_t* node6 = (node_t*) malloc(sizeof(node_t));
	node_t* node7 = (node_t*) malloc(sizeof(node_t));
	node_t* node8 = (node_t*) malloc(sizeof(node_t));

	node1->val = 10; node1->sig = node2;
	node2->val = 2; node2->sig = node3;
	node3->val = 2; node3->sig = node4;
	node4->val = 2; node4->sig = node5;
	node5->val = 3; node5->sig = node6;
	node6->val = 5; node6->sig = node7;
	node7->val = 5; node7->sig = node8;
	node8->val = 11; node8->sig = NULL;

	list_t* lista1 = (list_t*) malloc(sizeof(list_t));
	lista1->head = node1;
	lista1->tail = node8;
	lista1->size = 8;

	printf("Lista original: ");
	imprimir_lista(lista1);
	
	remover_consecutivos(lista1);
	printf("Resultado esperado: 10 -> 2 -> 3 -> 5 -> 11 -> NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(lista1);

	printf("\n=== TEST 2: Lista sin duplicados consecutivos ===\n");
	node_t* sin_dup1 = (node_t*) malloc(sizeof(node_t));
	node_t* sin_dup2 = (node_t*) malloc(sizeof(node_t));
	node_t* sin_dup3 = (node_t*) malloc(sizeof(node_t));
	node_t* sin_dup4 = (node_t*) malloc(sizeof(node_t));

	sin_dup1->val = 1; sin_dup1->sig = sin_dup2;
	sin_dup2->val = 3; sin_dup2->sig = sin_dup3;
	sin_dup3->val = 5; sin_dup3->sig = sin_dup4;
	sin_dup4->val = 7; sin_dup4->sig = NULL;

	list_t* lista2 = (list_t*) malloc(sizeof(list_t));
	lista2->head = sin_dup1;
	lista2->tail = sin_dup4;
	lista2->size = 4;

	printf("Lista original: ");
	imprimir_lista(lista2);
	
	remover_consecutivos(lista2);
	printf("Resultado esperado: 1 -> 3 -> 5 -> 7 -> NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(lista2);

	printf("\n=== TEST 3: Lista con todos los elementos iguales ===\n");
	node_t* igual1 = (node_t*) malloc(sizeof(node_t));
	node_t* igual2 = (node_t*) malloc(sizeof(node_t));
	node_t* igual3 = (node_t*) malloc(sizeof(node_t));
	node_t* igual4 = (node_t*) malloc(sizeof(node_t));
	node_t* igual5 = (node_t*) malloc(sizeof(node_t));

	igual1->val = 7; igual1->sig = igual2;
	igual2->val = 7; igual2->sig = igual3;
	igual3->val = 7; igual3->sig = igual4;
	igual4->val = 7; igual4->sig = igual5;
	igual5->val = 7; igual5->sig = NULL;

	list_t* lista3 = (list_t*) malloc(sizeof(list_t));
	lista3->head = igual1;
	lista3->tail = igual5;
	lista3->size = 5;

	printf("Lista original: ");
	imprimir_lista(lista3);
	
	remover_consecutivos(lista3);
	printf("Resultado esperado: 7 -> NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(lista3);

	printf("\n=== TEST 4: Lista con un solo elemento ===\n");
	node_t* single = (node_t*) malloc(sizeof(node_t));
	single->val = 42;
	single->sig = NULL;

	list_t* lista4 = (list_t*) malloc(sizeof(list_t));
	lista4->head = single;
	lista4->tail = single;
	lista4->size = 1;

	printf("Lista original: ");
	imprimir_lista(lista4);
	
	remover_consecutivos(lista4);
	printf("Resultado esperado: 42 -> NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(lista4);

	printf("\n=== TEST 5: Lista vacía ===\n");
	list_t* lista5 = (list_t*) malloc(sizeof(list_t));
	lista5->head = NULL;
	lista5->tail = NULL;
	lista5->size = 0;

	printf("Lista original: ");
	imprimir_lista(lista5);
	
	remover_consecutivos(lista5);
	printf("Resultado esperado: NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(lista5);

	printf("\n=== TEST 6: Duplicados al inicio ===\n");
	node_t* inicio1 = (node_t*) malloc(sizeof(node_t));
	node_t* inicio2 = (node_t*) malloc(sizeof(node_t));
	node_t* inicio3 = (node_t*) malloc(sizeof(node_t));
	node_t* inicio4 = (node_t*) malloc(sizeof(node_t));
	node_t* inicio5 = (node_t*) malloc(sizeof(node_t));

	inicio1->val = 1; inicio1->sig = inicio2;
	inicio2->val = 1; inicio2->sig = inicio3;
	inicio3->val = 1; inicio3->sig = inicio4;
	inicio4->val = 2; inicio4->sig = inicio5;
	inicio5->val = 3; inicio5->sig = NULL;

	list_t* lista6 = (list_t*) malloc(sizeof(list_t));
	lista6->head = inicio1;
	lista6->tail = inicio5;
	lista6->size = 5;

	printf("Lista original: ");
	imprimir_lista(lista6);
	
	remover_consecutivos(lista6);
	printf("Resultado esperado: 1 -> 2 -> 3 -> NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(lista6);

	printf("\n=== TEST 7: Duplicados al final ===\n");
	node_t* final1 = (node_t*) malloc(sizeof(node_t));
	node_t* final2 = (node_t*) malloc(sizeof(node_t));
	node_t* final3 = (node_t*) malloc(sizeof(node_t));
	node_t* final4 = (node_t*) malloc(sizeof(node_t));
	node_t* final5 = (node_t*) malloc(sizeof(node_t));

	final1->val = 1; final1->sig = final2;
	final2->val = 2; final2->sig = final3;
	final3->val = 9; final3->sig = final4;
	final4->val = 9; final4->sig = final5;
	final5->val = 9; final5->sig = NULL;

	list_t* lista7 = (list_t*) malloc(sizeof(list_t));
	lista7->head = final1;
	lista7->tail = final5;
	lista7->size = 5;

	printf("Lista original: ");
	imprimir_lista(lista7);
	
	remover_consecutivos(lista7);
	printf("Resultado esperado: 1 -> 2 -> 9 -> NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(lista7);

	printf("\n=== TEST 8: Múltiples grupos de duplicados ===\n");
	node_t* multi1 = (node_t*) malloc(sizeof(node_t));
	node_t* multi2 = (node_t*) malloc(sizeof(node_t));
	node_t* multi3 = (node_t*) malloc(sizeof(node_t));
	node_t* multi4 = (node_t*) malloc(sizeof(node_t));
	node_t* multi5 = (node_t*) malloc(sizeof(node_t));
	node_t* multi6 = (node_t*) malloc(sizeof(node_t));
	node_t* multi7 = (node_t*) malloc(sizeof(node_t));
	node_t* multi8 = (node_t*) malloc(sizeof(node_t));
	node_t* multi9 = (node_t*) malloc(sizeof(node_t));

	multi1->val = 1; multi1->sig = multi2;
	multi2->val = 1; multi2->sig = multi3;
	multi3->val = 2; multi3->sig = multi4;
	multi4->val = 3; multi4->sig = multi5;
	multi5->val = 3; multi5->sig = multi6;
	multi6->val = 3; multi6->sig = multi7;
	multi7->val = 4; multi7->sig = multi8;
	multi8->val = 5; multi8->sig = multi9;
	multi9->val = 5; multi9->sig = NULL;

	list_t* lista8 = (list_t*) malloc(sizeof(list_t));
	lista8->head = multi1;
	lista8->tail = multi9;
	lista8->size = 9;

	printf("Lista original: ");
	imprimir_lista(lista8);
	
	remover_consecutivos(lista8);
	printf("Resultado esperado: 1 -> 2 -> 3 -> 4 -> 5 -> NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(lista8);

	printf("\n=== TEST 9: Lista con dos elementos iguales ===\n");
	node_t* dos1 = (node_t*) malloc(sizeof(node_t));
	node_t* dos2 = (node_t*) malloc(sizeof(node_t));

	dos1->val = 5; dos1->sig = dos2;
	dos2->val = 5; dos2->sig = NULL;

	list_t* lista9 = (list_t*) malloc(sizeof(list_t));
	lista9->head = dos1;
	lista9->tail = dos2;
	lista9->size = 2;

	printf("Lista original: ");
	imprimir_lista(lista9);
	
	remover_consecutivos(lista9);
	printf("Resultado esperado: 5 -> NULL\n");
	printf("Resultado obtenido: ");
	imprimir_lista(lista9);

	printf("\n=== Liberando memoria ===\n");
	printf("Nota: En una implementación completa, se debería gestionar la memoria\n");
	printf("de los nodos que se eliminan durante el proceso de remover consecutivos.\n");
	printf("Además, se debería actualizar correctamente el campo 'size' y 'tail' de la lista.\n");
	
	// Liberar las estructuras de lista
	free(lista1); free(lista2); free(lista3); free(lista4); free(lista5);
	free(lista6); free(lista7); free(lista8); free(lista9);
	
	printf("\n¡Todas las pruebas completadas!\n");
}
