int maxValley(int H[], int n) {
    int i = 0, max_total = 0;

    while (i < n - 1) {
        // 1. Saltamos lo que no sea el inicio de una bajada
        while (i < n - 1 && H[i] <= H[i+1]){
            i++;
        } 

        int pasos = 1; // El punto donde estamos ya cuenta como el primero
        int bajo = 0, subio = 0;

        // 2. Bajamos y contamos
        while (i < n - 1 && H[i] > H[i+1]) {
            i++; 
            pasos++; 
            bajo = 1;
        }

        // 3. Subimos y contamos
        while (i < n - 1 && H[i] < H[i+1]) {
            i++; 
            pasos++; 
            subio = 1;
        }

        // Si realmente bajó y después subió, comparamos el tamaño
        if (bajo && subio) {
            if (pasos > max_total) max_total = pasos;
        }
        
    }
    return max_total;
}

int N = 4;

int foundWordInMatrix1() {
    char mat[N][N] = {
        {'C','A','T','F'},
        {'B','G','E','S'},
        {'I','T','A','E'},
        {'S','O','N','G'}
    };

    char palabra[] = "CAT";
    int len = strlen(palabra);
    int encontrada = 0;

    // Buscar horizontal
    for (int i = 0; i < N; i++) {
        for (int j = 0; j <= N - len; j++) {
            int k;
            for (k = 0; k < len; k++) {
                if (mat[i][j + k] != palabra[k])
                    break;
            }
            if (k == len) {
                encontrada = 1;
                break;
            }
        }
        if (encontrada) break;
    }

    // Buscar vertical (solo si no se encontró horizontal)
    if (!encontrada) {
        for (int j = 0; j < N; j++) {
            for (int i = 0; i <= N - len; i++) {
                int k;
                for (k = 0; k < len; k++) {
                    if (mat[i + k][j] != palabra[k])
                        break;
                }
                if (k == len) {
                    encontrada = 1;
                    break;
                }
            }
            if (encontrada) break;
        }
    }

}


// Direcciones: horizontal y vertical
int dx[] = {0, 1};
int dy[] = {1, 0};

int foundWordInMatrix2(char mat[N][N], int n, char palabra[]) {
    int len = strlen(palabra);

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int dir = 0; dir < 2; dir++) { // solo horizontal y vertical
                int k;
                for (k = 0; k < len; k++) {
                    int x = i + dx[dir] * k;
                    int y = j + dy[dir] * k;

                    // verificar límites
                    if (x < 0 ||  x >= n  || y < 0 || y >= n)
                        break;

                    if (mat[x][y] != palabra[k])
                        break;
                }
                if (k == len) return 1; // encontrada
            }
        }
    }
    return 0; // no encontrada
}


int maxSubarrayK1(int arr[], int n, int k) {
    int maxSum = 0;        // suma máxima encontrada
    int sum;
    
    for (int i = 0; i <= n - k; i++) {
        sum = 0;
        // calcular la suma del subarray desde i hasta i+k-1
        for (int j = i; j < i + k; j++) {
            sum += arr[j];
        }
        
        if (i == 0 || sum > maxSum)
            maxSum = sum;
    }
    
    return maxSum;
}


// Version optimizada usando sliding window
int maxSubarrayK2(int arr[], int n, int k) {
    int sum = 0;

    for (int i = 0; i < k; i++)
        sum += arr[i];

    int maxSum = sum;

    // mover ventana
    for (int i = k; i < n; i++) {
        sum = sum - arr[i - k] + arr[i];  // restar el que sale, sumar el que entra
        if (sum > maxSum)
            maxSum = sum;
    }

    return maxSum;
}
