class User:
    def __init__(self, user_id, name, email, user_type):
        self._user_id = user_id
        self._name = name
        self._email = email
        self._user_type = user_type

    @property
    def user_id(self):
        return self._user_id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def user_type(self):
        return self._user_type

    def __str__(self):
        return f"{self._name} - {self._email} - {self._user_type}"


class Student(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email, "student")
        self._enrolled_courses = []
        self._grades = {}

    @property
    def enrolled_courses(self):
        return self._enrolled_courses

    @property
    def grades(self):
        return self._grades

    def enroll_course(self, course_id):
        if course_id not in self._enrolled_courses:
            self._enrolled_courses.append(course_id)
            return True
        return False

    def record_grade(self, evaluation_id, grade):
        self._grades[evaluation_id] = grade


class Instructor(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email, "instructor")
        self._taught_courses = []

    @property
    def taught_courses(self):
        return self._taught_courses

    def add_course(self, course_id):
        if course_id not in self._taught_courses:
            self._taught_courses.append(course_id)


class Evaluation:
    def __init__(self, evaluation_id, course_id, name, evaluation_type, max_score):
        self._evaluation_id = evaluation_id
        self._course_id = course_id
        self._name = name
        self._evaluation_type = evaluation_type
        self._max_score = max_score
        self._grades = {}

    @property
    def evaluation_id(self):
        return self._evaluation_id

    @property
    def course_id(self):
        return self._course_id

    @property
    def name(self):
        return self._name

    @property
    def evaluation_type(self):
        return self._evaluation_type

    @property
    def max_score(self):
        return self._max_score

    def register_grade(self, student_id, grade):
        if 0 <= grade <= self._max_score:
            self._grades[student_id] = grade
            return True
        return False

    def get_grade(self, student_id):
        return self._grades.get(student_id, None)

    def __str__(self):
        return f"{self._name} - ({self._evaluation_type}) - Max score: {self._max_score}"


class Course:
    def __init__(self, course_id, name, code, instructor_id):
        self._course_id = course_id
        self._name = name
        self._code = code
        self._instructor_id = instructor_id
        self._enrolled_students = []
        self._evaluations = []

    @property
    def course_id(self):
        return self._course_id

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def instructor_id(self):
        return self._instructor_id

    @property
    def enrolled_students(self):
        return self._enrolled_students

    @property
    def evaluations(self):
        return self._evaluations

    def enroll_student(self, student_id):
        if student_id not in self._enrolled_students:
            self._enrolled_students.append(student_id)
            return True
        return False

    def add_evaluation(self, evaluation_id):
        if evaluation_id not in self._evaluations:
            self._evaluations.append(evaluation_id)

    def __str__(self):
        return f"{self._name} ({self._code})"


class CourseManagementSystem:
    def __init__(self):
        self._users = {}
        self._courses = {}
        self._evaluations = {}
        self.load_data()

    def load_data(self):
        self.load_users()
        self.load_courses()
        self.load_evaluations()
        self.load_grades()

    def save_data(self):
        self.save_users()
        self.save_courses()
        self.save_evaluations()
        self.save_grades()

    def load_users(self):
        try:
            with open("users.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        user_id, name, email, user_type = line.split("|")
                        if user_type == "student":
                            self._users[user_id] = Student(user_id, name, email)
                        elif user_type == "instructor":
                            self._users[user_id] = Instructor(user_id, name, email)
            print("Usuarios cargados desde users.txt")
        except FileNotFoundError:
            print("Archivo users.txt no encontrado")

    def save_users(self):
        with open("users.txt", "w", encoding="utf-8") as file:
            for user_id, user in self._users.items():
                file.write(f"{user_id}|{user.name}|{user.email}|{user.user_type}\n")

    def load_courses(self):
        try:
            with open("courses.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        course_id, name, code, instructor_id = line.split("|")
                        if instructor_id in self._users:
                            self._courses[course_id] = Course(course_id, name, code, instructor_id)
            print("Cursos cargados desde courses.txt")
        except FileNotFoundError:
            print("Archivo courses.txt no encontrado")

    def save_courses(self):
        with open("courses.txt", "w", encoding="utf-8") as file:
            for course_id, course in self._courses.items():
                file.write(f"{course_id}|{course.name}|{course.code}|{course.instructor_id}\n")

    def load_evaluations(self):
        try:
            with open("evaluations.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        eval_id, name, course_id, eval_type, max_score = line.split("|")
                        if course_id in self._courses:
                            self._evaluations[eval_id] = Evaluation(eval_id, course_id, name, eval_type, int(max_score))
            print("Evaluaciones cargadas desde evaluations.txt")
        except FileNotFoundError:
            print("Archivo evaluations.txt no encontrado")

    def save_evaluations(self):
        with open("evaluations.txt", "w", encoding="utf-8") as file:
            for eval_id, evaluation in self._evaluations.items():
                file.write(
                    f"{eval_id}|{evaluation.name}|{evaluation.course_id}|{evaluation.evaluation_type}|{evaluation.max_score}\n")

    def load_grades(self):
        try:
            with open("grades.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        student_id, eval_id, grade = line.split("|")
                        if student_id in self._users and eval_id in self._evaluations:
                            self._users[student_id].record_grade(eval_id, float(grade))
            print("Calificaciones cargadas desde grades.txt")
        except FileNotFoundError:
            print("Archivo grades.txt no encontrado")

    def save_grades(self):
        with open("grades.txt", "w", encoding="utf-8") as file:
            for user_id, user in self._users.items():
                if isinstance(user, Student):
                    for eval_id, grade in user.grades.items():
                        file.write(f"{user_id}|{eval_id}|{grade}\n")

    def id_exists(self, user_id):
        return user_id in self._users or user_id in self._courses or user_id in self._evaluations

    def email_exists(self, email):
        for user in self._users.values():
            if user.email == email:
                return True
        return False

    def course_code_exists(self, code):
        for course in self._courses.values():
            if course.code == code:
                return True
        return False

    def register_user(self, user_id, name, email, user_type):
        if self.id_exists(user_id):
            raise ValueError("El ID ya está en uso")

        if self.email_exists(email):
            raise ValueError("El email ya está registrado")

        if user_type == "student":
            self._users[user_id] = Student(user_id, name, email)
        elif user_type == "instructor":
            self._users[user_id] = Instructor(user_id, name, email)
        else:
            raise ValueError("Tipo de usuario no válido")
        self.save_data()

        return user_id

    def get_user(self, user_id):
        return self._users.get(user_id, None)

    def list_users(self, user_type=None):
        if user_type:
            return [user for user in self._users.values() if user.user_type == user_type]
        return list(self._users.values())

    def create_course(self, course_id, name, code, instructor_id):
        if self.id_exists(course_id):
            raise ValueError("El ID del curso ya está en uso")

        if instructor_id not in self._users or not isinstance(self._users[instructor_id], Instructor):
            raise ValueError("El instructor no existe")

        if self.course_code_exists(code):
            raise ValueError("El código del curso ya existe")

        self._courses[course_id] = Course(course_id, name, code, instructor_id)

        instructor = self._users[instructor_id]
        instructor.add_course(course_id)
        self.save_data()
        print(f"Curso {name} creado exitosamente")
        return course_id

    def get_course(self, course_id):
        return self._courses.get(course_id, None)

    def list_courses(self):
        return list(self._courses.values())

    def enroll_student_in_course(self, student_id, course_id):
        if student_id not in self._users or not isinstance(self._users[student_id], Student):
            raise ValueError("El estudiante no existe")

        if course_id not in self._courses:
            raise ValueError("El curso no existe")

        course = self._courses[course_id]
        if course.enroll_student(student_id):
            student = self._users[student_id]
            result = student.enroll_course(course_id)
            if result:
                self.save_data()
                print("Estudiante inscrito exitosamente en el curso")
            return result

        return False

    def get_enrolled_students(self, course_id):
        if course_id not in self._courses:
            raise ValueError("El curso no existe")

        course = self._courses[course_id]
        students = []
        for student_id in course.enrolled_students:
            if student_id in self._users:
                students.append(self._users[student_id])

        return students

    def create_evaluation(self, evaluation_id, course_id, name, evaluation_type, max_score):
        if self.id_exists(evaluation_id):
            raise ValueError("El ID de la evaluación ya está en uso")

        if course_id not in self._courses:
            raise ValueError("El curso no existe")

        if evaluation_type not in ["exam", "assignment"]:
            raise ValueError("Tipo de evaluación no válido")

        self._evaluations[evaluation_id] = Evaluation(evaluation_id, course_id, name, evaluation_type, max_score)

        course = self._courses[course_id]
        course.add_evaluation(evaluation_id)
        self.save_data()
        print(f"Evaluacion {name} creada exitosamente")

        return evaluation_id

    def get_evaluation(self, evaluation_id):
        return self._evaluations.get(evaluation_id, None)

    def list_course_evaluations(self, course_id):
        if course_id not in self._courses:
            raise ValueError("El curso no existe.")

        course = self._courses[course_id]
        evaluations = []
        for eval_id in course.evaluations:
            if eval_id in self._evaluations:
                evaluations.append(self._evaluations[eval_id])

        return evaluations

    def register_grade(self):
        print("\n--- REGISTRAR CALIFICACIÓN ---")
        student_id = input("Carnet del estudiante: ")
        evaluation_id = input("ID de la evaluación: ")

        if student_id not in self._users or not isinstance(self._users[student_id], Student):
            print("Error: No existe un estudiante con este carnet.")
            return

        if evaluation_id not in self._evaluations:
            print("Error: No existe una evaluación con este ID.")
            return

        try:
            grade = float(input("Calificación: "))
            evaluation = self._evaluations[evaluation_id]

            if grade < 0 or grade > evaluation.max_score:
                print(f"Error: La calificación debe estar entre 0 y {evaluation.max_score}")
                return

            student = self._users[student_id]

            if evaluation.course_id not in student.enrolled_courses:
                print("Error: El estudiante no está inscrito en este curso.")
                return

            if evaluation.register_grade(student_id, grade):
                student.record_grade(evaluation_id, grade)
                self.save_data()
                print(f"Calificación {grade}/{evaluation.max_score} registrada para {student.name}")
            else:
                print("Error al registrar la calificación")

        except ValueError:
            print("Error: La calificación debe ser un número.")

    def show_course_details(self):
        print("\n--- DETALLES DEL CURSO ---")
        course_id = input("ID del curso: ")

        if course_id not in self._courses:
            print("Error: No existe un curso con este ID.")
            return

        course = self._courses[course_id]
        print(f"\nCURSO: {course.name} ({course.code})")

        if course.instructor_id in self._users:
            instructor = self._users[course.instructor_id]
            print(f"Instructor: {instructor.name}")

        print(f"\nEstudiantes inscritos ({len(course.enrolled_students)}):")
        for student_id in course.enrolled_students:
            if student_id in self._users:
                student = self._users[student_id]
                print(f"  - {student.name} ({student_id})")

        print(f"\nEvaluaciones ({len(course.evaluations)}):")
        for eval_id in course.evaluations:
            if eval_id in self._evaluations:
                evaluation = self._evaluations[eval_id]
                print(f"  - {evaluation.name} (ID: {eval_id}, Max: {evaluation.max_score})")

    def show_student_grades(self):
        print("\n--- CALIFICACIONES DEL ESTUDIANTE ---")
        student_id = input("ID del estudiante: ")

        if student_id not in self._users or not isinstance(self._users[student_id], Student):
            print("Error: No existe un estudiante con este ID.")
            return

        student = self._users[student_id]
        print(f"\nCalificaciones de {student.name} ({student_id})")

        if not student.grades:
            print("No tiene calificaciones registradas.")
            return

        total_score = 0
        count = 0

        for eval_id, grade in student.grades.items():
            if eval_id in self._evaluations:
                evaluation = self._evaluations[eval_id]
                percentage = (grade / evaluation.max_score) * 100
                print(f"  - {evaluation.name}: {grade}/{evaluation.max_score} ({percentage:.2f}%)")
                total_score += grade
                count += 1

        if count > 0:
            average = total_score / count
            print(f"\nPromedio: {average:.2f}/100")

    def show_evaluation_results(self):
        print("\n--- RESULTADOS DE EVALUACIÓN ---")
        evaluation_id = input("ID de la evaluación: ")

        if evaluation_id not in self._evaluations:
            print("Error: No existe una evaluación con este ID.")
            return

        evaluation = self._evaluations[evaluation_id]
        course = self._courses.get(evaluation.course_id)

        print(f"\nEvaluación: {evaluation.name}")
        print(f"Curso: {course.name if course else 'Curso no encontrado'}")
        print(f"Tipo: {evaluation.evaluation_type}")
        print(f"Puntaje máximo: {evaluation.max_score}")

        grades = evaluation._grades
        if not grades:
            print("No hay calificaciones registradas para esta evaluación.")
            return

        print(f"\nCalificaciones registradas ({len(grades)}):")
        grade_values = []

        for student_id, grade in grades.items():
            if student_id in self._users:
                student = self._users[student_id]
                percentage = (grade / evaluation.max_score) * 100
                print(f"  - {student.name}: {grade}/{evaluation.max_score} ({percentage:.1f}%)")
                grade_values.append(percentage)

        if grade_values:
            avg_percentage = sum(grade_values) / len(grade_values)
            max_percentage = max(grade_values)
            min_percentage = min(grade_values)

            print(f"\nEstadísticas:")
            print(f"  - Promedio: {avg_percentage:.1f}%")
            print(f"  - Máxima: {max_percentage:.1f}%")
            print(f"  - Mínima: {min_percentage:.1f}%")

    def generate_low_performance_report(self, threshold=60):
        print(f"\n=== REPORTE: ESTUDIANTES CON RENDIMIENTO BAJO (<{threshold}) ===")

        found = False
        for student_id, student in self._users.items():
            if isinstance(student, Student) and student.grades:
                total_score = sum(student.grades.values())
                average = total_score / len(student.grades)

                if average < threshold:
                    print(f"\n{student.name} ({student_id})")
                    print(f"Promedio: {average:.2f}/100")
                    print(f"Cursos inscritos: {len(student.enrolled_courses)}")
                    print(f"Evaluaciones realizadas: {len(student.grades)}")
                    found = True

        if not found:
            print("No hay estudiantes con rendimiento bajo.")

    def generate_course_report(self):
        print("\n=== REPORTE POR CURSO ===")
        course_id = input("ID del curso: ")

        if course_id not in self._courses:
            print("Error: No existe un curso con este ID.")
            return

        course = self._courses[course_id]
        print(f"\nReporte del curso: {course.name} ({course.code})")

        if course.instructor_id in self._users:
            instructor = self._users[course.instructor_id]
            print(f"Instructor: {instructor.name}")

        print(f"Estudiantes inscritos: {len(course.enrolled_students)}")
        print(f"Evaluaciones: {len(course.evaluations)}")

        for eval_id in course.evaluations:
            if eval_id in self._evaluations:
                evaluation = self._evaluations[eval_id]
                grades = []

                for student_id in course.enrolled_students:
                    if student_id in self._users and eval_id in self._users[student_id].grades:
                        grades.append(self._users[student_id].grades[eval_id])
                if grades:
                    avg = sum(grades) / len(grades)
                    max_grade = max(grades)
                    min_grade = min(grades)
                    print(f"\n{evaluation.name}:")
                    print(f"Promedio: {avg:.2f}/{evaluation.max_score}")
                    print(f"Máxima: {max_grade}/{evaluation.max_score}")
                    print(f"Mínima: {min_grade}/{evaluation.max_score}")
                    print(f"Calificados: {len(grades)}/{len(course.enrolled_students)}")

    def generate_student_report(self):
        print("\n=== REPORTE INDIVIDUAL DE ESTUDIANTE ===")
        student_id = input("ID del estudiante: ")

        if student_id not in self._users or not isinstance(self._users[student_id], Student):
            print("Error: No existe un estudiante con este ID.")
            return

        student = self._users[student_id]
        print(f"\nReporte de: {student.name} ({student_id})")
        print(f"Cursos inscritos: {len(student.enrolled_courses)}")

        if student.grades:
            total = sum(student.grades.values())
            average = total / len(student.grades)
            print(f"Promedio general: {average:.2f}/100")

            print("\nCalificaciones por curso:")
            for course_id in student.enrolled_courses:
                if course_id in self._courses:
                    course = self._courses[course_id]
                    course_grades = []

                    for eval_id in course.evaluations:
                        if eval_id in student.grades:
                            course_grades.append(student.grades[eval_id])

                    if course_grades:
                        course_avg = sum(course_grades) / len(course_grades)
                        print(f"  - {course.name}: {course_avg:.2f}/100")
        else:
            print("No tiene calificaciones registradas.")

    def clear_all_data(self):
        print("\n--- LIMPIAR TODOS LOS DATOS ---")
        confirm = input("¿Estás seguro de que quieres borrar TODOS los datos? (escribe 'CONFIRMAR' para continuar): ")

        if confirm == "CONFIRMAR":
            self._users.clear()
            self._courses.clear()
            self._evaluations.clear()

            try:
                open("users.txt", "w").close()
                open("courses.txt", "w").close()
                open("evaluations.txt", "w").close()
                open("grades.txt", "w").close()
                print("Todos los datos han sido eliminados exitosamente.")
            except Exception as e:
                print(f"Error al limpiar archivos: {e}")
        else:
            print("Operación cancelada.")


system = CourseManagementSystem()

while True:
    print("       SISTEMA DE GESTIÓN DE CURSOS ONLINE")
    print("=" * 50)
    print("1. Registrar Estudiante")
    print("2. Registrar Instructor")
    print("3. Crear Curso")
    print("4. Inscribir Estudiante en Curso")
    print("5. Crear Evaluación")
    print("6. Registrar Calificación")
    print("7. Ver Detalles de Curso")
    print("8. Ver Calificaciones de Estudiante")
    print("9. Ver Resultados de Evaluación")
    print("10. Reporte: Estudiantes con Rendimiento Bajo")
    print("11. Reporte por Curso")
    print("12. Reporte Individual de Estudiante")
    print("13. Listar Usuarios")
    print("14. Listar Cursos")
    print("15. Limpiar Todos los Datos")
    print("16. Salir")
    option = input("Seleccione una opción: ")

    try:
        match option:
            case "1":
                print("\n--- REGISTRAR ESTUDIANTE ---")
                user_id = input("ID del estudiante: ")
                name = input("Nombre: ")
                email = input("Email: ")
                system.register_user(user_id, name, email, "student")

            case "2":
                print("\n--- REGISTRAR INSTRUCTOR ---")
                user_id = input("ID del instructor: ")
                name = input("Nombre: ")
                email = input("Email: ")
                system.register_user(user_id, name, email, "instructor")

            case "3":
                print("\n--- CREAR CURSO ---")
                course_id = input("ID del curso: ")
                name = input("Nombre del curso: ")
                code = input("Código del curso: ")
                instructor_id = input("ID del instructor: ")
                system.create_course(course_id, name, code, instructor_id)

            case "4":
                print("\n--- INSCRIBIR ESTUDIANTE EN CURSO ---")
                student_id = input("ID del estudiante: ")
                course_id = input("ID del curso: ")
                system.enroll_student_in_course(student_id, course_id)

            case "5":
                print("\n--- CREAR EVALUACIÓN ---")
                evaluation_id = input("ID de la evaluación: ")
                course_id = input("ID del curso: ")
                name = input("Nombre de la evaluación: ")
                eval_type = input("Tipo (examen/assignment): ")
                max_score = int(input("Puntaje máximo: "))
                system.create_evaluation(evaluation_id, course_id, name, eval_type, max_score)

            case "6":
                system.register_grade()

            case "7":
                system.show_course_details()

            case "8":
                system.show_student_grades()

            case "9":
                system.show_evaluation_results()

            case "10":
                threshold = input("Umbral de promedio (por defecto 60): ")
                threshold = int(threshold) if threshold else 60
                system.generate_low_performance_report(threshold)

            case "11":
                system.generate_course_report()

            case "12":
                system.generate_student_report()

            case "13":
                print("\n--- LISTA DE USUARIOS ---")
                users = system.list_users()
                for user in users:
                    print(f"- {user}")

            case "14":
                print("\n--- LISTA DE CURSOS ---")
                courses = system.list_courses()
                for course in courses:
                    print(f"- {course}")

            case "15":
                system.clear_all_data()

            case "16":
                print("¡Gracias por usar el sistema, adioooooooooos! ")
                break

            case _:
                print("Opción no válida. Intente de nuevo.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")