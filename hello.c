#include <cs50.h>
#include <stdio.h>

// .h is a header file

int main(void)
{
//    printf("hello, world\n");
    string answer = get_string("What is your name? ");
    printf("hello, %s\n", answer);
}