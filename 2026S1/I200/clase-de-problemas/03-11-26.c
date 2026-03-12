int maxVelley(int H[], int n) {
 int i = 0, max_total = 0;

 while (i < n-1 ){
   while (i < n - 1 && H[i] <= H[i+1]) i++; // ignoro lo que no es bajada

   int pasos = 1;
   int bajo = 0, subio = 0;

   while (i < n - 1 && H[i] > H[i+1]) {
     i++;
     pasos++;
     bajo = 1;
   }

 }
}