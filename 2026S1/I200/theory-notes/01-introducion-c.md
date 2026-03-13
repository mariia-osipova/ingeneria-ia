# Clase 1 – Introducción al lenguaje C - 05/03/2026

## Contenidos

- [Diferencias con Python](#diferencias-con-python)
- [Estructura del lenguaje](#estructura-del-lenguaje)
- [Definición de variables](#definición-de-variables)
- [Tipos nativos en C](#tipos-nativos-en-c)
- [Ciclos](#ciclos)
- [Funciones](#funciones)
- [Operadores](#operadores)
- [Imprimir y leer desde la consola](#imprimir-en-pantalla-y-leer-desde-la-consola)
- [Arreglos](#listas-y-vectores)
- [¿Cómo ejecuto mi código?](#cómo-ejecuto-mi-código)

---

## Objetivos de la clase

- Comprender las diferencias fundamentales entre C y Python.
- Introducir la estructura básica de un programa en C.
- Conocer los tipos de datos, ciclos, funciones y operadores.
- Aprender a compilar y ejecutar programas en C desde la consola.

---

## Diferencias con Python

### Lenguaje compilado vs lenguaje interpretado

**Python** es un lenguaje **interpretado**: el código es procesado por un intérprete que, en tiempo de ejecución, traduce cada instrucción a código máquina y la ejecuta.

**C** es un lenguaje **compilado**: un compilador traduce *todo* el código fuente a código máquina en tiempo de compilación y genera un archivo ejecutable. Dicho ejecutable puede luego ejecutarse directamente en la computadora.

> ⚠️ El código compilado es **específico para una arquitectura y un sistema operativo**. Por ejemplo, un ejecutable compilado en Windows para arquitectura Intel no puede ejecutarse directamente en macOS.

| | Python | C |
|---|---|---|
| Archivos | `.py` | `.c` |
| Ejecución | `python3 mi_codigo.py` | Compilar → ejecutar `./programa` |
| Errores | En tiempo de ejecución | Muchos detectados en compilación |

---

## Estructura del lenguaje

En **Python**, los bloques se definen por **indentación**:

```python
def main():
    for i in range(5):
        print(i)
    print("hola mundo")
```

En **C**, los bloques se definen con **llaves `{}`**:

```c
#include <stdio.h>

int main() {
    for (int i = 0; i < 5; i++) {
        printf("%d\n", i);
    }
    printf("hola mundo\n");
    return 0;
}
```

> 📌 La indentación en C no es obligatoria, pero se recomienda para legibilidad. Cada sentencia debe terminar con `;`.

---

## Definición de variables

En **Python**, el tipo puede cambiar libremente:

```python
myVar = 3
myVar = "tres"  # válido en Python
```

En **C**, el lenguaje es de **tipado estático**: el tipo debe declararse explícitamente y **no puede cambiar**:

```c
int myVar;
myVar = 3;

// O en una sola línea:
int myVar = 3;
```

> El compilador necesita conocer el tipo para reservar la cantidad correcta de memoria en el **stack** (la memoria usada durante la ejecución de una función, que se libera cuando la función termina).

---

## Tipos nativos en C

| Tipo | Uso principal |
|---|---|
| `char` | Caracteres |
| `int` | Enteros |
| `float` | Decimales |
| `double` | Decimales de mayor precisión |
| `void` | Sin tipo (funciones que no devuelven nada) |
| `short` | Enteros pequeños |
| `long` | Enteros grandes |
| `unsigned` | Solo valores positivos |

> 🔍 **Investigar:** `size_t` y su uso en C.

---

## Ciclos

### Ciclo `for`

**Python:**
```python
for i in range(5):
    print(i)
```

**C:**
```c
#include <stdio.h>

int main() {
    for (int i = 0; i < 5; i++) {
        printf("%d\n", i);
    }
    return 0;
}
```

### Ciclo `while`

**Python:**
```python
i = 0
while i < 5:
    print(i)
    i += 1
```

**C:**
```c
#include <stdio.h>

int main() {
    int i = 0;
    while (i < 5) {
        printf("%d\n", i);
        i++;
    }
    return 0;
}
```

---

## Funciones

**Python:**
```python
def myFunc(var1, var2):
    return var1 + var2
```

**C:** Se debe declarar el tipo de retorno y el tipo de cada parámetro:
```c
int myFunc(int var1, int var2) {
    return var1 + var2;
}
```

Si la función no devuelve nada, se usa `void` y no es necesario el `return`:

```c
void saludar() {
    printf("Hola!\n");
}
```

### La función `main`

En C siempre aparece la función `main`. El compilador necesita saber desde dónde comenzar la ejecución — ese punto de entrada es `main`.

```c
int main() {
    // código principal
    return 0;
}
```

> ❓ **Para pensar:** ¿Por qué la función `main` siempre devuelve `int`?

---

## Operadores

### Operadores aritméticos

| Operador | Python | C | Descripción |
|---|---|---|---|
| `+` | ✅ | ✅ | Suma |
| `-` | ✅ | ✅ | Resta |
| `*` | ✅ | ✅ | Multiplicación |
| `/` | ✅ | ✅ | División |
| `//` | ✅ | ❌ | División entera |
| `%` | ✅ | ✅ | Módulo |
| `**` | ✅ | ❌ | Potencia |

> En C, para potencias se usa `math.h`:
> ```c
> double resultado = pow(2, 3);
> ```

### Operadores de asignación

| Operador | Python | C |
|---|---|---|
| `=` | ✅ | ✅ |
| `+=` | ✅ | ✅ |
| `-=` | ✅ | ✅ |
| `*=` | ✅ | ✅ |
| `/=` | ✅ | ✅ |
| `%=` | ✅ | ✅ |

### Operadores de comparación

| Operador | Python | C |
|---|---|---|
| `==` | ✅ | ✅ |
| `!=` | ✅ | ✅ |
| `>` | ✅ | ✅ |
| `<` | ✅ | ✅ |
| `>=` | ✅ | ✅ |
| `<=` | ✅ | ✅ |

### Operadores lógicos

| Operador | Python | C |
|---|---|---|
| AND | `and` | `&&` |
| OR | `or` | `\|\|` |
| NOT | `not` | `!` |

### Operadores bit a bit

| Operador | Python | C |
|---|---|---|
| AND | `&` | `&` |
| OR | `\|` | `\|` |
| XOR | `^` | `^` |
| NOT | `~` | `~` |
| Shift izquierda | `<<` | `<<` |
| Shift derecha | `>>` | `>>` |

---

## Imprimir en pantalla y leer desde la consola

### Imprimir

**Python:**
```python
print("Hola mundo")
print("El número es:", 10)
```

**C** — usando `printf` de la librería `stdio.h`:
```c
#include <stdio.h>

int main() {
    printf("Hola mundo\n");
    printf("El número es: %d\n", 10);
    return 0;
}
```

| Especificador | Tipo |
|---|---|
| `%d` | Entero (`int`) |
| `%f` | Decimal (`float`, `double`) |
| `%c` | Carácter (`char`) |

> `\n` indica un salto de línea.

### Leer desde la consola

**Python:**
```python
edad = int(input("Ingrese su edad: "))
print("Edad:", edad)
```

**C** — usando `scanf`:
```c
#include <stdio.h>

int main() {
    int edad;
    printf("Ingrese su edad: ");
    scanf("%d", &edad);
    printf("Edad: %d\n", edad);
    return 0;
}
```

> `&edad` obtiene la **dirección de memoria** de la variable. `scanf` necesita esa dirección para almacenar el valor ingresado. El uso de punteros se verá en detalle más adelante.

---

## Listas y vectores

En C **no existen listas dinámicas** como en Python. Lo que existe son los **arreglos**: espacios contiguos de memoria con elementos del mismo tipo y tamaño fijo.

```c
// Sintaxis general
tipo nombre[tamaño];

// Ejemplo
int numeros[5] = {1, 2, 3, 4, 5};
```

> El tamaño es fijo y se define en tiempo de compilación.

### Acceso a los elementos

Los arreglos se indexan desde **0**:

```c
#include <stdio.h>

int main() {
    int numeros[5] = {1, 2, 3, 4, 5};
    for (int i = 0; i < 5; i++) {
        printf("%d\n", numeros[i]);
    }
    return 0;
}
```

### Tamaño de un arreglo

```c
int numeros[5];
int tamaño = sizeof(numeros) / sizeof(numeros[0]);
```

### ⚠️ Accesos fuera de rango

Si se intenta acceder a una posición inválida (ej: `numeros[6]`), el programa entra en **comportamiento indefinido**:

- puede parecer funcionar
- puede mostrar valores basura
- puede finalizar con un error grave

> En C, **el lenguaje no verifica los límites de los arreglos**. Es responsabilidad del programador evitar accesos fuera de rango.

---

## ¿Cómo ejecuto mi código?

### Compilar y ejecutar

```bash
gcc programa.c -o programa
./programa
```

### Compilación estricta (usada en la materia)

```bash
gcc -g -std=c99 -Wall -Wconversion -Wno-sign-conversion -Werror -o tp1 *.c -lm
```

| Flag | Descripción |
|---|---|
| `-g` | Permite debuggear con GDB |
| `-std=c99` | Fuerza el estándar C99 |
| `-Wall` | Activa la mayoría de las advertencias importantes |
| `-Wconversion` | Advierte sobre conversiones implícitas de tipos |
| `-Wno-sign-conversion` | Desactiva advertencias por conversiones entre tipos con y sin signo |
| `-Werror` | Convierte todas las advertencias en errores (si hay un warning, no compila) |
| `*.c` | Compila todos los archivos `.c` del directorio |
| `-lm` | Linkea la librería matemática |

> ⚠️ **Importante:** evitar usar el botón de "Run" de VSCode. Siempre compilar y ejecutar desde la **consola**.
