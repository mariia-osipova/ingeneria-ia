#include <stdio.h>
//hacer con el mod

int fast_exp(int base, int exp){

  printf("entrada: %d\n", exp);

  if (exp == 0){
    return 1;
  }

  int result = 0;

  if (exp % 2 == 0){
    result = fast_exp(base, exp/2);
    result = result * result;
  }
  else {
    result = fast_exp(base, exp/2);
    result = result * result * base;
  }

  printf("salida: %d\n", exp);
  return result;
}

int main(){
  printf("%d", fast_exp(2, 16));
}
