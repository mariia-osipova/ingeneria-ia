# Clase 2 – Memoria dinámica y punteros - 12/03/2026

## Contenidos

- [Repaso: memoria en tiempo de compilación](#repaso-memoria-en-tiempo-de-compilación)
- [¿Qué es la memoria dinámica?](#qué-es-la-memoria-dinámica)
- [Cómo imaginar la memoria](#cómo-imaginar-la-memoria)
- [Punteros](#punteros)
- [Reservar memoria dinámica con malloc](#reservar-memoria-dinámica-con-malloc)
- [Acceder al valor apuntado](#acceder-al-valor-apuntado)
- [Aritmética de punteros](#aritmética-de-punteros)
- [Relación entre arreglos y punteros](#relación-entre-arreglos-y-punteros)
- [Liberar la memoria](#liberar-la-memoria)
- [Valgrind](#valgrind)
- [Archivos .h (Header files)](#archivos-h-header-files)
- [Makefile](#makefile)

---

## Repaso: memoria en tiempo de compilación

En la clase anterior vimos que las variables declaradas en tiempo de compilación viven en la memoria **stack** (pila):

```c
int x = 5;
int arreglo[10];
```

En estos casos:
- El tamaño de la memoria se conoce **antes** de ejecutar el programa.
- La memoria se reserva y libera **automáticamente** al entrar y salir de las funciones.

> ❓ **Pero, ¿qué pasa si necesitamos memoria cuyo tamaño solo se conoce en tiempo de ejecución?**

Por ejemplo:
- El tamaño de un arreglo depende de un número ingresado por teclado.
- Leemos un archivo y no sabemos cuántos datos contiene.
- Necesitamos estructuras que crezcan o se achiquen dinámicamente.

Para estos casos existe la **memoria dinámica**.

---

## ¿Qué es la memoria dinámica?

La memoria dinámica es memoria que el programa **solicita al sistema operativo en tiempo de ejecución**. Esta memoria vive en una zona llamada **heap** (montículo).

| Característica | Stack | Heap |
|---|---|---|
| Tamaño | Se conoce al compilar | Se decide en ejecución |
| Liberación | Automática | Manual (responsabilidad del programador) |
| Gestión | El compilador | El programador |

---

## Cómo imaginar la memoria

Podemos pensar la memoria como un arreglo gigante de 1s y 0s:

- Cada bit es un `0` o un `1`.
- Cada **8 bits** forman **1 byte**.
- Cada byte tiene una **dirección de memoria única**.
- La dirección de memoria indica **dónde** está guardado un dato.

```
Dirección:  0x1000   0x1001   0x1002   0x1003  ...
Contenido:  [  42  ] [  0   ] [  17  ] [  5   ] ...
```

---

## Punteros

Un **puntero** es una variable que guarda una **dirección de memoria**, no un valor común como un `int` o un `float`.

```
Dirección: 0x1000 → valor: 42
Un puntero guarda 0x1000 para saber dónde está ese 42.
```

### Tamaño de los punteros

El tamaño de un puntero depende de la **arquitectura del sistema**, no del tipo al que apunta:

| Arquitectura | Tamaño del puntero |
|---|---|
| 32 bits | 4 bytes |
| 64 bits | 8 bytes |

> ❓ **Para pensar:** Si tengo un sistema de 32 bits, ¿cuántas direcciones de memoria distintas puedo representar?

### Tipo de los punteros

Los punteros tienen tipo. El tipo es importante para interpretar correctamente la memoria y para la aritmética de punteros:

```c
int* p;   // p es un puntero a entero
```

---

## Reservar memoria dinámica con `malloc`

Para pedir memoria dinámica usamos `malloc`, incluida en `stdlib.h`:

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int* misNumeros = malloc(sizeof(int) * 10);

    if (misNumeros == NULL) {
        printf("Error al reservar memoria\n");
        return 1;
    }

    return 0;
}
```

`malloc`:
- Reserva un bloque de memoria del tamaño indicado (en bytes).
- Devuelve un **puntero al inicio** del bloque.
- Si falla, devuelve **`NULL`**.

> ❓ **Para pensar:** ¿Por qué podría fallar el `malloc`?

---

## Acceder al valor apuntado

Para acceder al valor almacenado en la dirección a la que apunta un puntero usamos el operador `*`:

```c
misNumeros[0] = 10;
int primerValor = *misNumeros;
```

| Expresión | Significado |
|---|---|
| `misNumeros` | La **dirección** de memoria |
| `*misNumeros` | El **valor** almacenado en esa dirección |

---

## Aritmética de punteros

Si `misNumeros` apunta al primer entero del arreglo, podemos avanzar posiciones:

```c
*(misNumeros + 1)  // accede al segundo entero
*(misNumeros + 2)  // accede al tercero
```

> Aunque cada dirección representa 1 byte, al sumar `1` a un puntero se avanza `sizeof(tipo)` bytes. El compilador conoce el tipo y hace el cálculo automáticamente.

---

## Relación entre arreglos y punteros

Cuando declaramos un arreglo, su nombre se comporta como un puntero al primer elemento:

```c
int miArreglo[10];
```

Estas dos expresiones son **equivalentes**:

```c
miArreglo[2]
*(miArreglo + 2)
```

> El operador `[]` es simplemente una forma más cómoda de escribir aritmética de punteros (*syntactic sugar*).

---

## Liberar la memoria

Toda memoria reservada con `malloc` **debe liberarse** con `free`:

```c
free(misNumeros);
```

No hacerlo genera **fugas de memoria** (memory leaks).

> ⚠️ **Importante:**
> - La memoria declarada en tiempo de compilación (stack) se libera **automáticamente** cuando la función termina.
> - La memoria pedida con `malloc` (heap) se libera **únicamente** si el programador llama a `free`.

---

## Valgrind

**Valgrind** es una herramienta que permite analizar el uso de memoria de los programas y detectar errores comunes.

Con Valgrind se puede:
- Detectar **accesos a memoria inválida** (direcciones nunca reservadas).
- Verificar que toda la memoria pedida con `malloc` sea liberada con `free`.
- Identificar **fugas de memoria** (memory leaks).

### Instalación del entorno

Dado que Valgrind es una herramienta de Linux, en la materia trabajamos con **Ubuntu**:

| Sistema | Solución |
|---|---|
| Windows | Usar **WSL2** para ejecutar Ubuntu |
| macOS | Usar **Docker** con un entorno Linux |

### Uso

```bash
valgrind -s --error-exitcode=1 --leak-check=full --show-leak-kinds=all --track-origins=yes ./programa
```

Se le pasa el ejecutable al final del comando.

---

## Archivos .h (Header files)

En C, los programas suelen dividirse en varios archivos para mantener el código ordenado, reutilizable y fácil de mantener. Para eso se usan los **archivos de encabezado** (`.h`).

Un archivo `.h` se usa para **declarar**:
- Funciones
- Estructuras (`struct`)
- Tipos (`typedef`)
- Constantes (`#define`)
- Variables globales (en casos puntuales)

> 📌 En los archivos `.h` **no se escribe la implementación**, solo se indica qué existe y cómo se puede usar.

### Estructura típica

| Archivo | Contenido |
|---|---|
| `.h` | Declaraciones (el "qué") |
| `.c` | Implementaciones (el "cómo") |

### Ejemplo

**`suma.h`**
```c
int suma(int a, int b);
```

**`suma.c`**
```c
#include "suma.h"

int suma(int a, int b) {
    return a + b;
}
```

**`main.c`**
```c
#include <stdio.h>
#include "suma.h"

int main() {
    printf("%d\n", suma(2, 3));
    return 0;
}
```

De esta forma, `main.c` sabe que existe la función `suma` sin necesitar conocer cómo está implementada.

### ¿Por qué usar archivos `.h`?

- Permiten organizar el código en **módulos**.
- Facilitan el **trabajo en equipo**.
- Evitan **duplicar declaraciones**.
- Permiten **reutilizar código** en distintos programas.
- Hacen más clara la **interfaz pública** de un módulo.

> Podemos pensar un archivo `.h` como un **contrato**: define qué funciones y tipos ofrece un módulo, pero no cómo están implementados.

---

## Makefile

Cuando un programa crece y se divide en varios archivos, compilarlo manualmente es tedioso y propenso a errores. Para eso existe el **Makefile**.

Un Makefile define cómo se debe compilar el programa y qué dependencias existen entre sus archivos. La herramienta `make` lee este archivo y ejecuta automáticamente los comandos necesarios.

### Estructura básica

```makefile
objetivo: dependencias
	comando
```

| Parte | Descripción |
|---|---|
| `objetivo` | Archivo que se quiere generar |
| `dependencias` | Archivos necesarios para construir el objetivo |
| `comando` | Instrucción a ejecutar (debe comenzar con una **tabulación**) |

### Ejemplo simple

Para un programa con `main.c` y `suma.c`:

```makefile
programa:
	gcc main.c -o programa

clean:
	rm -f *.o programa
```

### Usar make

```bash
# Compilar el programa
make programa
# Ejecuta: gcc main.c -o programa

# Borrar los archivos generados
make clean
# Ejecuta: rm -f *.o programa
```

> `make` solo recompila los archivos que **cambiaron** desde la última compilación.