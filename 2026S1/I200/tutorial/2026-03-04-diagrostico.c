#include <cs50.h>
#include <stdio.h>

int Mayor(int a, int b, int c, int d)
{
    int may_num = a;

    if (b > may_num) may_num = b;
    if (c > may_num) may_num = c;
    if (d > may_num) may_num = d;

    return may_num;
}

int main(void)
{
    int a = get_int("Enter number a: ");
    int b = get_int("Enter number b: ");
    int c = get_int("Enter number c: ");
    int d = get_int("Enter number d: ");

    printf("De los %i, %i, %i, %i el mayor es %i\n", a, b, c, d, Mayor(a, b, c, d));
    return 0;
}
