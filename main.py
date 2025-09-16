class Usuario:
    def __init__(self, id, nombre, email, tipo):
        self._id = id
        self._nombre = nombre
        self._email = email
        self._tipo = tipo

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
        self._cursos_inscritos = []

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
        self._calificaciones = {}

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


class SistemaGestionCursos:
    def __init__(self):
        self._usuarios = {}
        self._cursos = {}
        self._evaluaciones = {}
        self._contador_ids = 1

    def _generar_id_unico(self):
        id_unico = f"id_{self._contador_ids}"
        self._contador_ids += 1
        return id_unico

    def _email_existe(self, email):
        for usuario in self._usuarios.values():
            if usuario.email == email:
                return True
        return False

    def _codigo_curso_existe(self, codigo):
        for curso in self._cursos.values():
            if curso.codigo == codigo:
                return True
        return False

    def registrar_usuario(self, nombre, email, tipo, **kwargs):
        if self._email_existe(email):
            raise ValueError("El email ya está registrado")

        usuario_id = self._generar_id_unico()

        if tipo == "estudiante":
            self._usuarios[usuario_id] = Estudiante(usuario_id, nombre, email)
        elif tipo == "instructor":
            self._usuarios[usuario_id] = Instructor(usuario_id, nombre, email)
        else:
            raise ValueError("Tipo de usuario no válido")

        return usuario_id

    def obtener_usuario(self, usuario_id):
        return self._usuarios.get(usuario_id, None)

    def listar_usuarios(self, tipo=None):
        if tipo:
            return [usuario for usuario in self._usuarios.values() if usuario.tipo == tipo]
        return list(self._usuarios.values())

    def crear_curso(self, nombre, codigo, instructor_id):
        if instructor_id not in self._usuarios or not isinstance(self._usuarios[instructor_id], Instructor):
            raise ValueError("El instructor no existe")

        if self._codigo_curso_existe(codigo):
            raise ValueError("El código del curso ya existe")

        curso_id = self._generar_id_unico()

        self._cursos[curso_id] = Curso(curso_id, nombre, codigo, instructor_id)

        instructor = self._usuarios[instructor_id]
        instructor.agregar_curso(curso_id)

        return curso_id

    def obtener_curso(self, curso_id):
        return self._cursos.get(curso_id, None)

    def listar_cursos(self):
        return list(self._cursos.values())

    def inscribir_estudiante_curso(self, estudiante_id, curso_id):
        if estudiante_id not in self._usuarios or not isinstance(self._usuarios[estudiante_id], Estudiante):
            raise ValueError("El estudiante no existe")

        if curso_id not in self._cursos:
            raise ValueError("El curso no existe")

        curso = self._cursos[curso_id]
        if curso.inscribir_estudiante(estudiante_id):
            estudiante = self._usuarios[estudiante_id]
            return estudiante.inscribir_curso(curso_id)

        return False

    def obtener_estudiantes_inscritos(self, curso_id):
        if curso_id not in self._cursos:
            raise ValueError("El curso no existe")

        curso = self._cursos[curso_id]
        estudiantes = []
        for estudiante_id in curso.estudiantes_inscritos:
            if estudiante_id in self._usuarios:
                estudiantes.append(self._usuarios[estudiante_id])

        return estudiantes

    def crear_evaluacion(self, curso_id, nombre, tipo, puntaje_maximo):
        if curso_id not in self._cursos:
            raise ValueError("El curso no existe")

        if tipo not in ["examen", "tarea"]:
            raise ValueError("Tipo de evaluación no válido")

        evaluacion_id = self._generar_id_unico()

        self._evaluaciones[evaluacion_id] = Evaluacion(evaluacion_id, curso_id, nombre, tipo, puntaje_maximo)

        curso = self._cursos[curso_id]
        curso.agregar_evaluacion(evaluacion_id)

        return evaluacion_id

    def obtener_evaluacion(self, evaluacion_id):
        return self._evaluaciones.get(evaluacion_id, None)

    def listar_evaluaciones_curso(self, curso_id):
        if curso_id not in self._cursos:
            raise ValueError("El curso no existe")

        curso = self._cursos[curso_id]
        evaluaciones = []
        for eval_id in curso.evaluaciones:
            if eval_id in self._evaluaciones:
                evaluaciones.append(self._evaluaciones[eval_id])

        return evaluaciones

#instancia
sistema = SistemaGestionCursos()


try:
    instructor1_id = sistema.registrar_usuario("Profesor Garcia", "garcia@gmail.com", "instructor")
    instructor2_id = sistema.registrar_usuario("Profesora Martinez", "martinez@gmail.com", "instructor")
    print(f"Instructores registrados: {instructor1_id}, {instructor2_id}")
except ValueError as e:
    print(f"Error al registrar instructor: {e}")

try:
    estudiante1_id = sistema.registrar_usuario("Ana Lopez", "ana@gmail.com", "estudiante")
    estudiante2_id = sistema.registrar_usuario("Carlos Ruiz", "carlos@gmail.com", "estudiante")
    estudiante3_id = sistema.registrar_usuario("Maria Torres", "maria@gmail.com", "estudiante")
    print(f"Estudiantes registrados: {estudiante1_id}, {estudiante2_id}, {estudiante3_id}")
except ValueError as e:
    print(f"Error al registrar estudiante: {e}")

#creacion de cursos

try:
    curso1_id = sistema.crear_curso("Pensamiento Computacional", "PROG101", instructor1_id)
    curso2_id = sistema.crear_curso("Precalculo", "MATH201", instructor2_id)
    print(f"Cursos creados: {curso1_id}, {curso2_id}")
except ValueError as e:
    print(f"Error al crear curso: {e}")

#inscripcion de estudiantes a cursos

try:
    sistema.inscribir_estudiante_curso(estudiante1_id, curso1_id)
    sistema.inscribir_estudiante_curso(estudiante2_id, curso1_id)
    sistema.inscribir_estudiante_curso(estudiante2_id, curso2_id)
    sistema.inscribir_estudiante_curso(estudiante3_id, curso2_id)
    print("Estudiantes inscritos exitosamente")
except ValueError as e:
    print(f"Error al inscribir estudiante: {e}")


#mostrar estudiantes inscritos por curso
print("\n=== Estudiantes Inscritos por curso ===")

cursos = sistema.listar_cursos()
for curso in cursos:
    print(f"\nEstudiantes en {curso.nombre}:")
    estudiantes = sistema.obtener_estudiantes_inscritos(curso.id)
    for estudiante in estudiantes:
        print(f"  - {estudiante.nombre}")

#mostrar cursos por estudiante
print("\n=== Cursos por estudinte ===")
estudiantes = sistema.listar_usuarios("estudiante")
for estudiante in estudiantes:
    print(f"\nCursos de {estudiante.nombre}:")
    for curso_id in estudiante.cursos_inscritos:
        curso = sistema.obtener_curso(curso_id)
        if curso:
            print(f"  - {curso.nombre}")

#creacion de evaluaciones
print("\n=== Creaciond e evaluaciones ===")

try:
    examen_prog_id = sistema.crear_evaluacion(curso1_id, "Examen Parcial", "examen", 100)
    tarea_prog_id = sistema.crear_evaluacion(curso1_id, "Tarea 1", "tarea", 50)
    examen_math_id = sistema.crear_evaluacion(curso2_id, "Examen Final", "examen", 100)
    print(f"Evaluaciones creadas: {examen_prog_id}, {tarea_prog_id}, {examen_math_id}")
except ValueError as e:
    print(f"Error al crear evaluación: {e}")


#registrar calificaciones
print("\n=== Registro de calificaciones ===")

examen_prog = sistema.obtener_evaluacion(examen_prog_id)
tarea_prog = sistema.obtener_evaluacion(tarea_prog_id)

if examen_prog:
    examen_prog.registrar_calificacion(estudiante1_id, 85)
    examen_prog.registrar_calificacion(estudiante2_id, 92)
    print("Calificaciones del examen de programación registradas")

if tarea_prog:
    tarea_prog.registrar_calificacion(estudiante1_id, 45)
    tarea_prog.registrar_calificacion(estudiante2_id, 48)
    print("Calificaciones de la tarea de programación registradas")

print("\n=== Consulta de calificaciones ===")

print(f"Calificacion de Ana en examen: {examen_prog.obtener_calificacion(estudiante1_id)}")
print(f"Calificacion de Carlos en examen: {examen_prog.obtener_calificacion(estudiante2_id)}")
print(f"Calificacion de Ana en tarea: {tarea_prog.obtener_calificacion(estudiante1_id)}")


print(f"Total usuarios: {len(sistema.listar_usuarios())}")
print(f"Total cursos: {len(sistema.listar_cursos())}")
print(f"Total evaluaciones: {len(sistema._evaluaciones)}")
