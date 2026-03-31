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

void print_list(Node *list) {
    while (list) {
        printf("%d", list->data);
        if (list->next) printf(" -> ");
        list = list->next;
    }
    printf("\n");
}

void free_list(Node *list) {
    Node *aux;
    while (list) { aux = list->next; free(list); list = aux; }
}

/* Returns a new sorted list containing only the elements
   that appear in both a and b (both lists must be sorted).
   Uses a two-pointer approach similar to the merge step in merge sort:
   - if a->data == b->data  =>  add to result, advance both
   - if a->data <  b->data  =>  advance a
   - if a->data >  b->data  =>  advance b */
Node *sorted_intersection(Node *a, Node *b) {
    Node dummy;          // dummy head to simplify building the result
    Node *tail = &dummy;
    dummy.next = NULL;

    while (a != NULL && b != NULL) {
        if (a->data == b->data) {
            tail->next = new_node(a->data);
            tail = tail->next;
            a = a->next;
            b = b->next;
        } else if (a->data < b->data) {
            a = a->next;
        } else {
            b = b->next;
        }
    }

    return dummy.next;
}

int main(void) {
    // a: 1 -> 3 -> 5 -> 7 -> 9
    Node *a = new_node(1);
    a->next = new_node(3);
    a->next->next = new_node(5);
    a->next->next->next = new_node(7);
    a->next->next->next->next = new_node(9);

    // b: 2 -> 3 -> 5 -> 6 -> 9 -> 10
    Node *b = new_node(2);
    b->next = new_node(3);
    b->next->next = new_node(5);
    b->next->next->next = new_node(6);
    b->next->next->next->next = new_node(9);
    b->next->next->next->next->next = new_node(10);

    printf("List a:        "); print_list(a);
    printf("List b:        "); print_list(b);

    Node *result = sorted_intersection(a, b);
    printf("Intersection:  "); print_list(result);  // Expected: 3 -> 5 -> 9

    free_list(a);
    free_list(b);
    free_list(result);
    return 0;
}
