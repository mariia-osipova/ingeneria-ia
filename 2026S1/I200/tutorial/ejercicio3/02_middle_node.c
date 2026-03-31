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

/* Returns the middle node using slow/fast pointers.
   If the list has even length, returns the second middle node. */
Node *middle_node(Node *list) {
    if (list == NULL) return NULL;

    Node *slow = list;
    Node *fast = list;

    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;
    }

    return slow;
}

int main(void) {
    // Odd length: 1 -> 2 -> 3 -> 4 -> 5  =>  middle = 3
    Node *list = new_node(1);
    list->next = new_node(2);
    list->next->next = new_node(3);
    list->next->next->next = new_node(4);
    list->next->next->next->next = new_node(5);

    printf("Middle (odd list):  %d\n", middle_node(list)->data);  // Expected: 3

    // Even length: 1 -> 2 -> 3 -> 4  =>  middle = 3 (second middle)
    Node *list2 = new_node(1);
    list2->next = new_node(2);
    list2->next->next = new_node(3);
    list2->next->next->next = new_node(4);

    printf("Middle (even list): %d\n", middle_node(list2)->data); // Expected: 3

    Node *aux;
    while (list)  { aux = list->next;  free(list);  list  = aux; }
    while (list2) { aux = list2->next; free(list2); list2 = aux; }
    return 0;
}
