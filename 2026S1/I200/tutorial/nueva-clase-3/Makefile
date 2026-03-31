CC = gcc
CFLAGS = -std=c99 -Wall -Wextra -g

all: ejercicios

ejercicios: ejercicios.c
	$(CC) $(CFLAGS) -o ejercicios ejercicios.c

valgrind: ejercicios
	valgrind --leak-check=full --error-exitcode=1 ./ejercicios

docker:
	docker build -t practica3 .
	docker run --rm practica3

clean:
	rm -f ejercicios

.PHONY: all clean valgrind docker
