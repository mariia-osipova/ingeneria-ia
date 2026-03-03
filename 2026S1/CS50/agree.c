#include <stdio.h>
#include <cs50.h>

int main(void)
{
  char c = get_char("Do you agree? (y/n): ");

  if (c == 'y' || c == 'Y')
  {
    printf("You agreed!\n");
  }
  else if (c == 'n')
  {
    printf("You disagreed!\n");
  }
  else
  {
    printf("invalid input! u stupid\n");
  }
}