#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

Node *new_node(int data) {
    Node *n = malloc(sizeof(Node));
    n->data = data;
    n->next = NULL;
    return n;
}

int length(Node *list) {
    int count = 0;
    while (list != NULL) {
        count++;
        list = list->next;
    }
    return count;
}

int main(void) {
    // List: 1 -> 2 -> 3 -> 4 -> 5
    Node *list = new_node(1);
    list->next = new_node(2);
    list->next->next = new_node(3);
    list->next->next->next = new_node(4);
    list->next->next->next->next = new_node(5);

    printf("Length: %d\n", length(list));  // Expected: 5

    Node *aux;
    while (list) {
        aux = list->next;
        free(list);
        list = aux;
    }
    return 0;
}
