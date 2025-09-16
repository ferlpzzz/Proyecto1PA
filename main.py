class Usuario:
    def __init__(self, id, nombre, email, tipo):
        self._id = id
        self._nombre = nombre
        self._email = email
        self._tipo = tipo #puede ser estudiante o instructor

        @property
        def id(self):
            return self._id

        @property
        def nombre(self):
            return self._nombre

        @property
        def email(self):
            return self._email

        @property
        def tipo(self):
            return self._tipo

        def __str__(self):
            return f"{self._nombre} - {self._email} - {self._tipo}"


class Estudiante(Usuario):
    def __init__(self, id, nombre, email):
        super().__init__(id, nombre, email, "estudiante")
        self._cursos_inscritos = []  #lista para cursos

    @property
    def cursos_inscritos(self):
        return self._cursos_inscritos

    def inscribir_curso(self, curso_id):
        if curso_id not in self._cursos_inscritos:
            self._cursos_inscritos.append(curso_id)
            return True
        return False
