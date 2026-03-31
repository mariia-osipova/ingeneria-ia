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

/* Returns 1 if the list has a cycle, 0 otherwise.
   Uses Floyd's slow/fast pointer algorithm:
   - slow moves one step at a time
   - fast moves two steps at a time
   - if they ever meet, there is a cycle */
int has_cycle(Node *list) {
    Node *slow = list;
    Node *fast = list;

    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;

        if (slow == fast)
            return 1;
    }

    return 0;
}

int main(void) {
    // No cycle: 1 -> 2 -> 3 -> 4 -> 5 -> NULL
    Node *list = new_node(1);
    list->next = new_node(2);
    list->next->next = new_node(3);
    list->next->next->next = new_node(4);
    list->next->next->next->next = new_node(5);

    printf("Has cycle (no cycle):   %s\n", has_cycle(list) ? "yes" : "no");  // Expected: no

    // With cycle: 1 -> 2 -> 3 -> 4 -> 5 -> (back to node 3)
    Node *cycle_list = new_node(1);
    cycle_list->next = new_node(2);
    cycle_list->next->next = new_node(3);
    cycle_list->next->next->next = new_node(4);
    cycle_list->next->next->next->next = new_node(5);
    cycle_list->next->next->next->next->next = cycle_list->next->next; // cycle

    printf("Has cycle (with cycle): %s\n", has_cycle(cycle_list) ? "yes" : "no"); // Expected: yes

    // Free only the non-cycle list (freeing a cycle list is tricky without extra logic)
    Node *aux;
    while (list) { aux = list->next; free(list); list = aux; }

    // For the cycle list: manually free the 5 nodes
    Node *nodes[5];
    nodes[0] = cycle_list;
    for (int i = 1; i < 5; i++) nodes[i] = nodes[i-1]->next;
    nodes[4]->next = NULL; // break the cycle before freeing
    for (int i = 0; i < 5; i++) free(nodes[i]);

    return 0;
}
