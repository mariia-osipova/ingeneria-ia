/**
 * Práctica 3 - Lenguaje C: Macros, Strings y Structs
 * ====================================================
 *
 * Tema unificador: Sistema de Agenda de Contactos
 *
 * En esta práctica vas a construir, paso a paso, una agenda de contactos.
 * Cada ejercicio depende del anterior, así que resolvelos en orden.
 *
 * Compilar:  gcc -std=c99 -Wall -Wextra -g -o ejercicios ejercicios.c
 * Ejecutar:  ./ejercicios
 * Valgrind:  valgrind --leak-check=full ./ejercicios
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ========================================================================
 * FRAMEWORK DE PRUEBAS
 * ======================================================================== */

static int tests_totales = 0;
static int tests_ok = 0;
static int tests_fail = 0;

#define TEST(nombre) do { \
    tests_totales++; \
    printf("  [TEST] %-50s ", nombre); \
} while(0)

#define ASSERT_EQ_INT(esperado, obtenido) do { \
    int _e = (esperado), _o = (obtenido); \
    if (_e == _o) { \
        printf("OK\n"); tests_ok++; \
    } else { \
        printf("FAIL (esperado: %d, obtenido: %d)\n", _e, _o); \
        tests_fail++; \
    } \
} while(0)

#define ASSERT_EQ_STR(esperado, obtenido) do { \
    const char* _e = (esperado); \
    const char* _o = (obtenido); \
    if (_e == NULL && _o == NULL) { \
        printf("OK\n"); tests_ok++; \
    } else if (_e && _o && strcmp(_e, _o) == 0) { \
        printf("OK\n"); tests_ok++; \
    } else { \
        printf("FAIL (esperado: \"%s\", obtenido: \"%s\")\n", \
               _e ? _e : "NULL", _o ? _o : "NULL"); \
        tests_fail++; \
    } \
} while(0)

#define ASSERT_TRUE(cond) do { \
    if (cond) { \
        printf("OK\n"); tests_ok++; \
    } else { \
        printf("FAIL (condicion falsa)\n"); \
        tests_fail++; \
    } \
} while(0)

#define ASSERT_NULL(ptr) do { \
    if ((ptr) == NULL) { \
        printf("OK\n"); tests_ok++; \
    } else { \
        printf("FAIL (esperado NULL, obtenido %p)\n", (void*)(ptr)); \
        tests_fail++; \
    } \
} while(0)

#define ASSERT_NOT_NULL(ptr) do { \
    if ((ptr) != NULL) { \
        printf("OK\n"); tests_ok++; \
    } else { \
        printf("FAIL (esperado no-NULL, obtenido NULL)\n"); \
        tests_fail++; \
    } \
} while(0)

#define SECCION(nombre) printf("\n=== %s ===\n", nombre)

/* ========================================================================
 * ESTRUCTURAS
 * ======================================================================== */

typedef struct {
    char* nombre;       // Nombre del contacto (memoria dinámica)
    char* telefono;     // Teléfono (memoria dinámica)
    char* email;        // Email (memoria dinámica, puede ser NULL)
} Contacto;

typedef struct {
    Contacto** contactos;   // Array dinámico de punteros a Contacto
    int cantidad;            // Cantidad actual de contactos
    int capacidad;           // Capacidad del array
} Agenda;

/* ========================================================================
 * EJERCICIO 1: Funciones de strings desde cero
 * ========================================================================
 *
 * ENUNCIADO:
 * Implementá las siguientes funciones SIN usar las funciones de <string.h>
 * (excepto en los tests).
 *
 * a) mi_strlen: Devuelve la longitud del string (sin contar el '\0').
 *    Pensá: ¿qué pasa si recibís un puntero NULL?
 *
 * b) mi_strcpy: Copia el string src en dst (incluyendo el '\0').
 *    Devuelve dst. Asumí que dst tiene espacio suficiente.
 *

 * IMPORTANTE: Prestá especial atención al rol del '\0'. Es lo que marca
 * dónde termina un string en C. Sin '\0', funciones como printf o strcmp
 * van a leer memoria basura hasta encontrar un cero por casualidad.
 */

int mi_strlen(const char* str) {
    // TODO: implementar
    (void)str;
    return 0;
}

char* mi_strcpy(char* dst, const char* src) {
    // TODO: implementar
    (void)src;
    return dst;
}


void test_ejercicio_1(void) {
    SECCION("EJERCICIO 1: Funciones de strings");

    // mi_strlen
    TEST("mi_strlen de string vacío");
    ASSERT_EQ_INT(0, mi_strlen(""));

    TEST("mi_strlen de \"hola\"");
    ASSERT_EQ_INT(4, mi_strlen("hola"));

    TEST("mi_strlen de string con espacios");
    ASSERT_EQ_INT(11, mi_strlen("hola mundo!"));

    TEST("mi_strlen con NULL devuelve -1");
    ASSERT_EQ_INT(-1, mi_strlen(NULL));

    // mi_strcpy - acá se ve la importancia del \0
    char buffer[20];
    memset(buffer, 'X', sizeof(buffer)); // Llenamos con basura

    TEST("mi_strcpy copia contenido");
    mi_strcpy(buffer, "test");
    ASSERT_EQ_STR("test", buffer);

    TEST("mi_strcpy pone \\0 al final");
    ASSERT_EQ_INT('\0', buffer[4]); // El \0 DEBE estar ahí

    TEST("mi_strcpy de string vacío");
    mi_strcpy(buffer, "");
    ASSERT_EQ_INT('\0', buffer[0]);
}

/* ========================================================================
 * EJERCICIO 2: Duplicar y concatenar strings con memoria dinámica
 * ========================================================================
 *
 * ENUNCIADO:
 * a) mi_strdup: Crea una COPIA del string en memoria dinámica (malloc).
 *    - Calculá cuánta memoria necesitás: strlen + 1 (¡por el '\0'!).
 *    - Si str es NULL, devolvé NULL.
 *    - El llamador es responsable de liberar la memoria.
 *
 * b) mi_strconcat: Concatena dos strings en un NUEVO string en el heap.
 *    - El resultado debe tener espacio para ambos strings + '\0'.
 *    - Si alguno es NULL, tratalo como string vacío.
 *    - El llamador es responsable de liberar la memoria.
 *
 * TRAMPA CLÁSICA: Si malloc pide strlen(str) bytes en vez de
 * strlen(str) + 1, el '\0' queda afuera. Valgrind lo detecta como
 * escritura fuera de bounds.
 */

char* mi_strdup(const char* str) {
    // TODO: implementar
    (void)str;
    return NULL;
}

char* mi_strconcat(const char* s1, const char* s2) {
    // TODO: implementar
    (void)s1;
    (void)s2;
    return NULL;
}

void test_ejercicio_2(void) {
    SECCION("EJERCICIO 2: Duplicar y concatenar strings");

    // mi_strdup
    TEST("mi_strdup copia el contenido");
    char* dup = mi_strdup("hola");
    ASSERT_EQ_STR("hola", dup);

    TEST("mi_strdup devuelve memoria nueva (no el mismo puntero)");
    ASSERT_TRUE((void*)dup != (void*)"hola"); // Debe ser otra dirección
    free(dup);

    TEST("mi_strdup de string vacío");
    dup = mi_strdup("");
    ASSERT_EQ_STR("", dup);

    TEST("mi_strdup de string vacío: \\0 presente");
    if (dup) {
        ASSERT_EQ_INT('\0', dup[0]);
    } else {
        printf("FAIL (dup es NULL)\n"); tests_fail++;
    }
    free(dup);

    TEST("mi_strdup de NULL devuelve NULL");
    ASSERT_NULL(mi_strdup(NULL));

    // mi_strconcat
    TEST("mi_strconcat de dos strings");
    char* concat = mi_strconcat("hola", " mundo");
    ASSERT_EQ_STR("hola mundo", concat);
    free(concat);

    TEST("mi_strconcat con primer NULL");
    concat = mi_strconcat(NULL, "mundo");
    ASSERT_EQ_STR("mundo", concat);
    free(concat);

    TEST("mi_strconcat con segundo NULL");
    concat = mi_strconcat("hola", NULL);
    ASSERT_EQ_STR("hola", concat);
    free(concat);

    TEST("mi_strconcat con ambos vacíos");
    concat = mi_strconcat("", "");
    ASSERT_EQ_STR("", concat);
    free(concat);
}

/* ========================================================================
 * EJERCICIO 3: Crear y destruir un Contacto
 * ========================================================================
 *
 * ENUNCIADO:
 * a) crear_contacto: Recibe nombre, teléfono y email (cualquiera puede
 *    ser NULL). Devuelve un puntero a un Contacto nuevo en el heap.
 *    - El Contacto debe tener COPIAS de los strings (no los punteros
 *      originales). Usá mi_strdup del ejercicio anterior.
 *    - Si nombre o teléfono son NULL, devolvé NULL (son obligatorios).
 *    - Email es opcional: si es NULL, guardá NULL.
 *
 * b) destruir_contacto: Libera TODA la memoria asociada al contacto.
 *    - Hay que liberar cada string Y el struct en sí.
 *    - Si recibe NULL, no hace nada.
 *
 * ATENCIÓN A LA MEMORIA:
 * Un Contacto tiene 4 bloques de memoria: el struct + 3 strings.
 * Si te olvidás de liberar alguno, Valgrind te va a reportar un leak.
 * Si email es NULL, son 3 bloques. ¿Tu destruir_contacto maneja eso?
 */

Contacto* crear_contacto(const char* nombre, const char* telefono, const char* email) {
    // TODO: implementar
    (void)nombre;
    (void)telefono;
    (void)email;
    return NULL;
}

void destruir_contacto(Contacto* c) {
    // TODO: implementar
    (void)c;
}

void test_ejercicio_3(void) {
    SECCION("EJERCICIO 3: Crear y destruir Contacto");

    TEST("crear_contacto devuelve no-NULL");
    Contacto* c = crear_contacto("Ana", "1234", "ana@mail.com");
    ASSERT_NOT_NULL(c);

    if (c) {
        TEST("nombre se copió correctamente");
        ASSERT_EQ_STR("Ana", c->nombre);

        TEST("teléfono se copió correctamente");
        ASSERT_EQ_STR("1234", c->telefono);

        TEST("email se copió correctamente");
        ASSERT_EQ_STR("ana@mail.com", c->email);

        // Verificar que son COPIAS, no los mismos punteros
        const char* nombre_orig = "Ana";
        TEST("nombre es una copia (distinto puntero)");
        ASSERT_TRUE(c->nombre != nombre_orig);

        destruir_contacto(c);
    }

    TEST("crear_contacto con email NULL");
    c = crear_contacto("Bob", "5678", NULL);
    ASSERT_NOT_NULL(c);
    if (c) {
        TEST("email es NULL cuando se pasa NULL");
        ASSERT_NULL(c->email);
        destruir_contacto(c);
    }

    TEST("crear_contacto con nombre NULL devuelve NULL");
    ASSERT_NULL(crear_contacto(NULL, "1234", "x@y.com"));

    TEST("crear_contacto con teléfono NULL devuelve NULL");
    ASSERT_NULL(crear_contacto("Ana", NULL, "x@y.com"));

    // destruir_contacto con NULL no debería crashear
    TEST("destruir_contacto(NULL) no crashea");
    destruir_contacto(NULL);
    ASSERT_TRUE(1); // Si llegamos acá, no crasheó
}

/* ========================================================================
 * EJERCICIO 4: Agenda - agregar y buscar contactos
 * ========================================================================
 *
 * ENUNCIADO:
 * a) crear_agenda: Crea una agenda vacía con una capacidad inicial dada.
 *    - Reservá memoria para la Agenda y para el array de punteros.
 *    - Inicializá cantidad en 0 y capacidad según el parámetro.
 *
 * b) agenda_agregar: Agrega un contacto a la agenda.
 *    - Recibe nombre, teléfono y email, y crea el contacto internamente.
 *    - Si la agenda está llena, duplicá la capacidad con realloc.
 *    - Devuelve 0 si tuvo éxito, -1 si falló.
 *
 * c) agenda_buscar: Busca un contacto por nombre.
 *    - Devuelve un puntero al Contacto encontrado (NO una copia).
 *    - Si no lo encuentra, devuelve NULL.
 *
 * COMPLEJIDAD DE MEMORIA:
 * La agenda tiene: 1 struct Agenda + 1 array de punteros (que crece con
 * realloc) + N contactos (cada uno con sus strings). Pensá cuántos
 * mallocs hay cuando la agenda tiene 3 contactos con email.
 * Respuesta: 1 (Agenda) + 1 (array) + 3 * (1 struct + 3 strings) = 14
 */

Agenda* crear_agenda(int capacidad_inicial) {
    // TODO: implementar
    (void)capacidad_inicial;
    return NULL;
}

int agenda_agregar(Agenda* agenda, const char* nombre, const char* telefono, const char* email) {
    // TODO: implementar
    (void)agenda;
    (void)nombre;
    (void)telefono;
    (void)email;
    return -1;
}

Contacto* agenda_buscar(Agenda* agenda, const char* nombre) {
    // TODO: implementar
    (void)agenda;
    (void)nombre;
    return NULL;
}

void test_ejercicio_4(void) {
    SECCION("EJERCICIO 4: Agenda - agregar y buscar");

    TEST("crear_agenda devuelve no-NULL");
    Agenda* ag = crear_agenda(2);
    ASSERT_NOT_NULL(ag);

    if (!ag) return;

    TEST("agenda vacía tiene cantidad 0");
    ASSERT_EQ_INT(0, ag->cantidad);

    TEST("capacidad inicial correcta");
    ASSERT_EQ_INT(2, ag->capacidad);

    TEST("agregar primer contacto");
    ASSERT_EQ_INT(0, agenda_agregar(ag, "Ana", "1111", "ana@mail.com"));

    TEST("cantidad después de agregar");
    ASSERT_EQ_INT(1, ag->cantidad);

    TEST("agregar segundo contacto");
    ASSERT_EQ_INT(0, agenda_agregar(ag, "Bob", "2222", NULL));

    TEST("agregar tercero (requiere realloc)");
    ASSERT_EQ_INT(0, agenda_agregar(ag, "Carlos", "3333", "carlos@mail.com"));

    TEST("capacidad creció después de realloc");
    ASSERT_TRUE(ag->capacidad >= 3);

    TEST("buscar contacto existente");
    Contacto* encontrado = agenda_buscar(ag, "Bob");
    ASSERT_NOT_NULL(encontrado);

    if (encontrado) {
        TEST("contacto encontrado tiene datos correctos");
        ASSERT_EQ_STR("2222", encontrado->telefono);
    }

    TEST("buscar contacto inexistente");
    ASSERT_NULL(agenda_buscar(ag, "Zoe"));

    // Limpieza (se testea en ejercicio 5)
    for (int i = 0; i < ag->cantidad; i++) {
        destruir_contacto(ag->contactos[i]);
    }
    free(ag->contactos);
    free(ag);
}

/* ========================================================================
 * EJERCICIO 5: Destruir y duplicar la agenda completa
 * ========================================================================
 *
 * ENUNCIADO:
 * a) destruir_agenda: Libera TODA la memoria de la agenda.
 *    - Cada contacto (con sus strings), el array de punteros, y la agenda.
 *    - Si recibe NULL, no hace nada.
 *
 * b) duplicar_agenda: Crea una copia PROFUNDA (deep copy) de la agenda.
 *    - La nueva agenda debe ser completamente independiente de la original.
 *    - Si modificás un contacto en la copia, la original no cambia.
 *    - Duplicá cada contacto (no copies los punteros).
 *
 * ESTE ES EL EJERCICIO MÁS DIFÍCIL:
 * Una deep copy de la agenda implica copiar:
 *   - La struct Agenda
 *   - El array de punteros a Contacto
 *   - Cada struct Contacto
 *   - Cada string dentro de cada Contacto
 * Si algo falla a mitad de camino (por ejemplo, el malloc del tercer
 * contacto falla), ¿liberás lo que ya pediste o dejás un memory leak?
 */

void destruir_agenda(Agenda* agenda) {
    // TODO: implementar
    (void)agenda;
}

Agenda* duplicar_agenda(Agenda* agenda) {
    // TODO: implementar
    (void)agenda;
    return NULL;
}

void test_ejercicio_5(void) {
    SECCION("EJERCICIO 5: Destruir y duplicar agenda");

    Agenda* ag = crear_agenda(2);
    if (!ag) {
        printf("  Skipping: crear_agenda no implementada\n");
        return;
    }

    agenda_agregar(ag, "Ana", "1111", "ana@mail.com");
    agenda_agregar(ag, "Bob", "2222", NULL);
    agenda_agregar(ag, "Carlos", "3333", "carlos@mail.com");

    // Test duplicar
    TEST("duplicar_agenda devuelve no-NULL");
    Agenda* copia = duplicar_agenda(ag);
    ASSERT_NOT_NULL(copia);

    if (copia) {
        TEST("copia tiene misma cantidad");
        ASSERT_EQ_INT(ag->cantidad, copia->cantidad);

        TEST("copia tiene los mismos datos");
        Contacto* c = agenda_buscar(copia, "Ana");
        ASSERT_NOT_NULL(c);

        if (c) {
            TEST("datos del contacto copiado son correctos");
            ASSERT_EQ_STR("ana@mail.com", c->email);

            TEST("contacto copiado es independiente (distinto puntero)");
            Contacto* orig = agenda_buscar(ag, "Ana");
            ASSERT_TRUE(c != orig);

            TEST("string copiado es independiente (distinto puntero)");
            ASSERT_TRUE(c->nombre != orig->nombre);
        }

        TEST("contacto con email NULL se duplica bien");
        Contacto* bob_copia = agenda_buscar(copia, "Bob");
        ASSERT_NOT_NULL(bob_copia);
        if (bob_copia) {
            TEST("email NULL se mantiene NULL en la copia");
            ASSERT_NULL(bob_copia->email);
        }

        destruir_agenda(copia);
    }

    // Test destruir (si Valgrind pasa sin leaks, está bien)
    TEST("destruir_agenda no crashea");
    destruir_agenda(ag);
    ASSERT_TRUE(1);

    TEST("destruir_agenda(NULL) no crashea");
    destruir_agenda(NULL);
    ASSERT_TRUE(1);
}

/* ========================================================================
 * MAIN
 * ======================================================================== */

int main(void) {
    printf("Práctica 3: Agenda de Contactos\n");
    printf("================================\n");

    test_ejercicio_1();
    test_ejercicio_2();
    test_ejercicio_3();
    test_ejercicio_4();
    test_ejercicio_5();

    printf("\n================================\n");
    printf("Resultados: %d/%d tests pasaron", tests_ok, tests_totales);
    if (tests_fail > 0) {
        printf(" (%d fallaron)", tests_fail);
    }
    printf("\n");

    if (tests_fail > 0) {
        printf("Ejecutá con valgrind para verificar memoria:\n");
        printf("  valgrind --leak-check=full ./ejercicios\n");
    } else {
        printf("Todos los tests pasaron! Verificá con valgrind:\n");
        printf("  valgrind --leak-check=full ./ejercicios\n");
    }

    return tests_fail > 0 ? 1 : 0;
}
