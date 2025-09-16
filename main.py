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

class Instructor(Usuario):
    def __init__(self, id, nombre, email):
        super().__init__(id, nombre, email, "instructor")
        self._cursos_impartidos = []

    @property
    def cursos_impartidos(self):
        return self._cursos_impartidos

    def agregar_curso(self, curso_id):
        if curso_id not in self._cursos_impartidos:
            self._cursos_impartidos.append(curso_id)

class Evaluacion:
    def __init__(self, id, curso_id, nombre, tipo, puntaje_maximo):
        self._id = id
        self._curso_id = curso_id
        self._nombre = nombre
        self._tipo = tipo
        self._puntaje_maximo = puntaje_maximo
        self._calificaciones = {} #diccionario para califidaciones (estudiante_id: calificacion=


    @property
    def id(self):
        return self._id

    @property
    def curso_id(self):
        return self._curso_id

    @property
    def nombre(self):
        return self._nombre

    @property
    def tipo(self):
        return self._tipo

    def registrar_calificacion(self, estudiante_id, calificacion):
        if 0 <= calificacion <= self._puntaje_maximo:
            self._calificaciones[estudiante_id] = calificacion
            return True
        return False

    def obtener_calificacion(self, estudiante_id):
        return self._calificaciones.get(estudiante_id, None)

    def __str__(self):
        return f"{self._nombre} - ({self._tipo}) - Puntaje maximo: {self._puntaje_maximo}"

class Curso:
    def __init__(self, id, nombre, codigo, instructor_id):
        self._id = id
        self._nombre = nombre
        self._codigo = codigo
        self._instructor_id = instructor_id
        self._estudiantes_inscritos = []
        self._evaluaciones = []

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def codigo(self):
        return self._codigo

    @property
    def instructor_id(self):
        return self._instructor_id

    @property
    def estudiantes_inscritos(self):
        return self._estudiantes_inscritos

    @property
    def evaluaciones(self):
        return self._evaluaciones

    def inscribir_estudiante(self, estudiante_id):
        if estudiante_id not in self.estudiantes_inscritos:
            self.estudiantes_inscritos.append(estudiante_id)
            return True
        return False

    def agregar_evaluacion(self, evaluacion_id):
        if evaluacion_id not in self.evaluaciones:
            self.evaluaciones.append(evaluacion_id)

    def __str__(self):
        return f"{self._nombre} ({self._codigo})"