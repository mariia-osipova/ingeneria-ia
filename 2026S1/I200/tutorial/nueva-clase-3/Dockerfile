FROM ubuntu
RUN apt update -y && apt upgrade -y
RUN apt install gcc valgrind make -y
COPY . /practica
WORKDIR /practica
CMD make ejercicios && valgrind --leak-check=full --error-exitcode=1 ./ejercicios
