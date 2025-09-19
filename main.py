class User:
    def __init__(self, user_id, name, email, user_type):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.user_type = user_type

    def __str__(self):
        return f"{self.name} - {self.email} - {self.user_type}"


class Student(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email, "estudiante")
        self.enrolled_courses = []
        self.grades = {}


class Instructor(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email, "instructor")
        self.taught_courses = []


class Course:
    def __init__(self, course_id, name, code, instructor_id):
        self.course_id = course_id
        self.name = name
        self.code = code
        self.instructor_id = instructor_id
        self.enrolled_students = []
        self.evaluations = []

    def __str__(self):
        return f"{self.name} ({self.code})"


class Evaluation:
    def __init__(self, evaluation_id, course_id, name, evaluation_type, max_score):
        self.evaluation_id = evaluation_id
        self.course_id = course_id
        self.name = name
        self.evaluation_type = evaluation_type
        self.max_score = max_score
        self.grades = {}

    def __str__(self):
        return f"{self.name} - ({self.evaluation_type}) - Max: {self.max_score}"


class CourseManagementSystem:
    def __init__(self):
        self.users = {}
        self.courses = {}
        self.evaluations = {}
        self.load_data()

    def load_data(self):
        files = [("users.txt", self.load_users), ("courses.txt", self.load_courses),
                 ("evaluations.txt", self.load_evaluations), ("grades.txt", self.load_grades)]

        for filename, loader in files:
            try:
                loader()
            except FileNotFoundError:
                pass

    def load_users(self):
        with open("users.txt", "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    user_id, name, email, user_type = line.strip().split("|")
                    if user_type == "estudiante":
                        self.users[user_id] = Student(user_id, name, email)
                    elif user_type == "instructor":
                        self.users[user_id] = Instructor(user_id, name, email)

    def load_courses(self):
        with open("courses.txt", "r", encoding="utf-8") as file:
            for line in file:
                if line.strip() and "|" in line:
                    parts = line.strip().split("|")
                    if len(parts) == 4:
                        course_id, name, code, instructor_id = parts
                        if instructor_id in self.users:
                            course = Course(course_id, name, code, instructor_id)
                            self.courses[course_id] = course
                            self.users[instructor_id].taught_courses.append(course_id)

    def load_evaluations(self):
        with open("evaluations.txt", "r", encoding="utf-8") as file:
            for line in file:
                if line.strip() and "|" in line:
                    eval_id, name, course_id, eval_type, max_score = line.strip().split("|")
                    if course_id in self.courses:
                        evaluation = Evaluation(eval_id, course_id, name, eval_type, int(max_score))
                        self.evaluations[eval_id] = evaluation
                        self.courses[course_id].evaluations.append(eval_id)

    def load_grades(self):
        with open("grades.txt", "r", encoding="utf-8") as file:
            for line in file:
                if line.strip() and "|" in line:
                    student_id, eval_id, grade = line.strip().split("|")
                    if student_id in self.users and eval_id in self.evaluations:
                        self.users[student_id].grades[eval_id] = float(grade)
                        self.evaluations[eval_id].grades[student_id] = float(grade)

    def save_data(self):
        with open("users.txt", "w", encoding="utf-8") as file:
            for user in self.users.values():
                file.write(f"{user.user_id}|{user.name}|{user.email}|{user.user_type}\n")

        with open("courses.txt", "w", encoding="utf-8") as file:
            for course in self.courses.values():
                file.write(f"{course.course_id}|{course.name}|{course.code}|{course.instructor_id}\n")

        with open("evaluations.txt", "w", encoding="utf-8") as file:
            for evaluation in self.evaluations.values():
                file.write(
                    f"{evaluation.evaluation_id}|{evaluation.name}|{evaluation.course_id}|{evaluation.evaluation_type}|{evaluation.max_score}\n")

        with open("grades.txt", "w", encoding="utf-8") as file:
            for user_id, user in self.users.items():
                if isinstance(user, Student):
                    for eval_id, grade in user.grades.items():
                        file.write(f"{user_id}|{eval_id}|{grade}\n")

    def safe_input(self, prompt, input_type="str"):
        while True:
            try:
                value = input(prompt)
                if input_type == "int":
                    return int(value)
                elif input_type == "float":
                    return float(value)
                else:
                    return value.strip()
            except ValueError:
                print("Error: Ingrese un valor válido")
            except KeyboardInterrupt:
                print("\nOperación cancelada")
                return None
        if user_id in self.users or user_id in self.courses or user_id in self.evaluations:
            raise ValueError("El ID ya está en uso")

        for user in self.users.values():
            if user.email == email:
                raise ValueError("El email ya está registrado")

        if user_type == "estudiante":
            self.users[user_id] = Student(user_id, name, email)
        elif user_type == "instructor":
            self.users[user_id] = Instructor(user_id, name, email)
        else:
            raise ValueError("Tipo de usuario no válido")

        self.save_data()
        print(f"{user_type.title()} registrado exitosamente")

    def create_course(self, course_id, name, code, instructor_id):
        if course_id in self.users or course_id in self.courses or course_id in self.evaluations:
            raise ValueError("El ID ya está en uso")

        if instructor_id not in self.users or not isinstance(self.users[instructor_id], Instructor):
            raise ValueError("El instructor no existe")

        for course in self.courses.values():
            if course.code == code:
                raise ValueError("El código del curso ya existe")

        course = Course(course_id, name, code, instructor_id)
        self.courses[course_id] = course
        self.users[instructor_id].taught_courses.append(course_id)
        self.save_data()
        print(f"Curso {name} creado exitosamente")

    def create_evaluation(self, evaluation_id, course_id, name, evaluation_type, max_score):
        if evaluation_id in self.users or evaluation_id in self.courses or evaluation_id in self.evaluations:
            raise ValueError("El ID ya está en uso")

        if course_id not in self.courses:
            raise ValueError("El curso no existe")

        if evaluation_type not in ["examen", "tarea"]:
            raise ValueError("Tipo de evaluación no válido")

        evaluation = Evaluation(evaluation_id, course_id, name, evaluation_type, max_score)
        self.evaluations[evaluation_id] = evaluation
        self.courses[course_id].evaluations.append(evaluation_id)
        self.save_data()
        print(f"Evaluación {name} creada exitosamente")

    def enroll_student(self, student_id, course_id):
        if student_id not in self.users or not isinstance(self.users[student_id], Student):
            raise ValueError("El estudiante no existe")

        if course_id not in self.courses:
            raise ValueError("El curso no existe")

        student = self.users[student_id]
        course = self.courses[course_id]

        if course_id in student.enrolled_courses:
            print("El estudiante ya está inscrito")
            return

        student.enrolled_courses.append(course_id)
        course.enrolled_students.append(student_id)
        self.save_data()
        print("Estudiante inscrito exitosamente")

    def register_grade(self, student_id, evaluation_id, grade):
        if student_id not in self.users or not isinstance(self.users[student_id], Student):
            raise ValueError("El estudiante no existe")

        if evaluation_id not in self.evaluations:
            raise ValueError("La evaluación no existe")

        evaluation = self.evaluations[evaluation_id]
        student = self.users[student_id]

        if evaluation.course_id not in student.enrolled_courses:
            raise ValueError("El estudiante no está inscrito en este curso")

        if grade < 0 or grade > evaluation.max_score:
            raise ValueError(f"La calificación debe estar entre 0 y {evaluation.max_score}")

        student.grades[evaluation_id] = grade
        evaluation.grades[student_id] = grade
        self.save_data()
        print(f"Calificación registrada: {grade}/{evaluation.max_score}")

    def show_student_grades(self, student_id):
        if student_id not in self.users or not isinstance(self.users[student_id], Student):
            print("El estudiante no existe")
            return

        student = self.users[student_id]
        print(f"\nCalificaciones de {student.name}:")

        if not student.grades:
            print("No tiene calificaciones")
            return

        total = 0
        count = 0
        for eval_id, grade in student.grades.items():
            if eval_id in self.evaluations:
                evaluation = self.evaluations[eval_id]
                percentage = (grade / evaluation.max_score) * 100
                print(f"- {evaluation.name}: {grade}/{evaluation.max_score} ({percentage:.1f}%)")
                total += grade
                count += 1

        if count > 0:
            print(f"Promedio: {total / count:.2f}")

    def show_course_details(self, course_id):
        if course_id not in self.courses:
            print("El curso no existe")
            return

        course = self.courses[course_id]
        instructor = self.users.get(course.instructor_id)

        print(f"\nCurso: {course.name} ({course.code})")
        print(f"Instructor: {instructor.name if instructor else 'No encontrado'}")
        print(f"Estudiantes: {len(course.enrolled_students)}")
        print(f"Evaluaciones: {len(course.evaluations)}")

    def list_items(self, item_type):
        if item_type == "users":
            if not self.users:
                print("No hay usuarios registrados")
                return
            for user in self.users.values():
                print(f"- [{user.user_id}] {user}")
        elif item_type == "students":
            students = [u for u in self.users.values() if isinstance(u, Student)]
            if not students:
                print("No hay estudiantes registrados")
                return
            for student in students:
                print(f"- [{student.user_id}] {student}")
        elif item_type == "instructors":
            instructors = [u for u in self.users.values() if isinstance(u, Instructor)]
            if not instructors:
                print("No hay instructores registrados")
                return
            for instructor in instructors:
                print(f"- [{instructor.user_id}] {instructor}")
        elif item_type == "courses":
            if not self.courses:
                print("No hay cursos registrados")
                return
            for course in self.courses.values():
                instructor = self.users.get(course.instructor_id)
                instructor_name = instructor.name if instructor else "No encontrado"
                print(f"- [{course.course_id}] {course} - {instructor_name}")

    def clear_all_data(self):
        confirm = input("¿Estás seguro? Escribe 'CONFIRMAR': ")
        if confirm == "CONFIRMAR":
            self.users.clear()
            self.courses.clear()
            self.evaluations.clear()
            for filename in ["users.txt", "courses.txt", "evaluations.txt", "grades.txt"]:
                open(filename, "w").close()
            print("Todos los datos eliminados")
        else:
            print("Operación cancelada")


system = CourseManagementSystem()

while True:
    print("\n" + "=" * 40)
    print("  SISTEMA DE GESTIÓN DE CURSOS")
    print("=" * 40)
    print("1. Usuarios  2. Cursos  3. Evaluaciones")
    print("4. Reportes  5. Limpiar  6. Salir")

    option = input("Opción: ")

    try:
        match option:
            case "1":
                print("\n1. Registrar Estudiante  2. Registrar Instructor")
                print("3. Listar Usuarios  4. Listar Estudiantes  5. Listar Instructores")
                sub = input("Opción: ")
                match sub:
                    case "1":
                        user_id = system.safe_input("ID: ")
                        if user_id is None: continue
                        name = system.safe_input("Nombre: ")
                        if name is None: continue
                        email = system.safe_input("Email: ")
                        if email is None: continue
                        system.register_user(user_id, name, email, "estudiante")
                    case "2":
                        user_id = system.safe_input("ID: ")
                        if user_id is None: continue
                        name = system.safe_input("Nombre: ")
                        if name is None: continue
                        email = system.safe_input("Email: ")
                        if email is None: continue
                        system.register_user(user_id, name, email, "instructor")
                    case "3":
                        system.list_items("users")
                    case "4":
                        system.list_items("students")
                    case "5":
                        system.list_items("instructors")
                    case _:
                        print("Opción no válida. Seleccione del 1 al 5.")

            case "2":
                print("\n1. Crear Curso  2. Inscribir Estudiante  3. Ver Detalles  4. Listar Cursos")
                sub = input("Opción: ")
                match sub:
                    case "1":
                        course_id = input("ID curso: ")
                        name = input("Nombre: ")
                        code = input("Código: ")
                        instructor_id = input("ID instructor: ")
                        system.create_course(course_id, name, code, instructor_id)
                    case "2":
                        student_id = input("ID estudiante: ")
                        course_id = input("ID curso: ")
                        system.enroll_student(student_id, course_id)
                    case "3":
                        course_id = input("ID curso: ")
                        system.show_course_details(course_id)
                    case "4":
                        system.list_items("courses")
                    case _:
                        print("Opción no válida. Seleccione del 1 al 4.")

            case "3":
                print("\n1. Crear Evaluación  2. Registrar Calificación  3. Ver Calificaciones")
                sub = input("Opción: ")
                match sub:
                    case "1":
                        eval_id = input("ID evaluación: ")
                        course_id = input("ID curso: ")
                        name = input("Nombre: ")
                        eval_type = system.safe_input("Tipo (examen/tarea): ")
                        if eval_type is None: continue
                        max_score = system.safe_input("Puntaje máximo: ", "int")
                        if max_score is None: continue
                        system.create_evaluation(eval_id, course_id, name, eval_type, max_score)
                    case "2":
                        student_id = input("ID estudiante: ")
                        eval_id = input("ID evaluación: ")
                        grade = float(input("Calificación: "))
                        system.register_grade(student_id, eval_id, grade)
                    case "3":
                        student_id = system.safe_input("ID estudiante: ")
                        if student_id is None: continue
                        system.show_student_grades(student_id)
                    case _:
                        print("Opción no válida. Seleccione del 1 al 3.")

            case "4":
                print("\n1. Estudiantes con bajo rendimiento")
                print("2. Reporte de curso")
                print("3. Reporte de estudiante")
                sub = input("Opción: ")
                match sub:
                    case "1":
                        threshold = input("Umbral (60): ")
                        threshold = float(threshold) if threshold else 60
                        print(f"\nEstudiantes con promedio < {threshold}:")
                        found = False
                        for student in system.users.values():
                            if isinstance(student, Student) and student.grades:
                                total = sum(student.grades.values())
                                avg = total / len(student.grades)
                                if avg < threshold:
                                    print(f"- {student.name}: {avg:.1f}")
                                    found = True
                        if not found:
                            print("No se encontraron estudiantes con rendimiento bajo")
                    case "2":
                        course_id = system.safe_input("ID curso: ")
                        if course_id is None: continue
                        system.show_course_details(course_id)
                    case "3":
                        student_id = system.safe_input("ID estudiante: ")
                        if student_id is None: continue
                        system.show_student_grades(student_id)
                    case _:
                        print("Opción no válida. Seleccione del 1 al 3.")

            case "5":
                system.clear_all_data()

            case "6":
                print("¡BYEEEEEEEEEEEEE!")
                break

            case _:
                print("Opción no válida. Seleccione del 1 al 6.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")