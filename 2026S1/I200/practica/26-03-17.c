#include <stdio.h>

struct Humano {int edad;};

void cambiar_edad_1(struct Humano *cesar, int edad_1){
  (*cesar).edad = edad_1;
}

struct Humano cambiar_edad_2(struct Humano juli, int edad_2){
  juli.edad = edad_2;
  return juli;
}

void cambiar_edad_3(struct Humano *jere, int edad_3){
  *jere = cambiar_edad_2(*jere, edad_3);
}


int main () {
  struct Humano mari;
  cambiar_edad_1(&mari, 5);
  printf("%d\n", mari.edad);

  cambiar_edad_2(mari, 55);
  printf("%d\n", mari.edad);

  cambiar_edad_3(&mari, 555);
  printf("%d\n", mari.edad);
}