class Estudiante:
    def __init__(self, nombre, nivel_de_estudio = 0, nivel_de_estres = 0):
        self.nombre = nombre
        self.nivel_de_estudio = nivel_de_estudio
        self.nivel_de_estres = nivel_de_estres

        # self.hora_estudio = 0
        # self.hora_descanso = 0

        # self.result = self.rendir_examen(result)
        #
        # self.nivel_result_estudio = self.nivel_result(nivel_de_estudio)
        # self.nivel_result_estres = self.nivel_result_estudio(nivel_estres)

    # def horas(self):
    #     self.hora_estudio = 0
    #     self.hora_descanso = 0

    def estudio(self, hora_estudio):
        self.nivel_de_estudio += hora_estudio * 5
        self.nivel_de_estres += hora_estudio * 2

        # return self.nivel_de_estudio, self.nivel_estres

    def descanso(self, hora_descanso):
        self.nivel_de_estudio += hora_descanso * (-0.5)
        # if self.nivel_de_estudio < 0:
        #     self.nivel_de_estudio = abs(self.nivel_de_estudio)
        self.nivel_de_estres += hora_descanso * (-3)
        # if self.nivel_de_estudio < 0:
        #     self.nivel_de_estudio = abs(self.nivel_de_estudio)

        # return self.nivel_de_estudio, self.nivel_estres

    # def nivel_result(self):
    #     self.nivel_result_estudio = self.descanso() + self.estudio()
    #     self.nivel_result_estres = self.descanso() + self.estudio()
    #
    #     return self.nivel_result_estudio, self.nivel_result_estres

    def rendir_examen(self):
        return self.nivel_de_estudio - (self.nivel_de_estres/2)


def main():
    sofocles = Estudiante("Sofocles", 5, 100)
    result = sofocles.rendir_examen()
    if result < 0:
        result = abs(result)
    print(f"el resultado es: {result} y el estres es {sofocles.nivel_de_estres}")

if __name__ == '__main__':
    main()




