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

    @property
    def enrolled_courses(self):
        return self._enrolled_courses

    def enroll_course(self, course_id):
        if course_id not in self._enrolled_courses:
            self._enrolled_courses.append(course_id)
            return True
        return False


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
        if student_id not in self.enrolled_students:
            self.enrolled_students.append(student_id)
            return True
        return False

    def add_evaluation(self, evaluation_id):
        if evaluation_id not in self.evaluations:
            self.evaluations.append(evaluation_id)

    def __str__(self):
        return f"{self._name} ({self._code})"


class CourseManagementSystem:
    def __init__(self):
        self._users = {}
        self._courses = {}
        self._evaluations = {}
        self._id_counter = 1

    def _generate_unique_id(self):
        unique_id = f"id_{self._id_counter}"
        self._id_counter += 1
        return unique_id

    def _email_exists(self, email):
        for user in self._users.values():
            if user.email == email:
                return True
        return False

    def _course_code_exists(self, code):
        for course in self._courses.values():
            if course.code == code:
                return True
        return False

    def register_user(self, name, email, user_type, **kwargs):
        if self._email_exists(email):
            raise ValueError("El email ya está registrado")

        user_id = self._generate_unique_id()

        if user_type == "student":
            self._users[user_id] = Student(user_id, name, email)
        elif user_type == "instructor":
            self._users[user_id] = Instructor(user_id, name, email)
        else:
            raise ValueError("Tipo de usuario no válido")

        return user_id

    def get_user(self, user_id):
        return self._users.get(user_id, None)

    def list_users(self, user_type=None):
        if user_type:
            return [user for user in self._users.values() if user.user_type == user_type]
        return list(self._users.values())

    def create_course(self, name, code, instructor_id):
        if instructor_id not in self._users or not isinstance(self._users[instructor_id], Instructor):
            raise ValueError("El instructor no existe")

        if self._course_code_exists(code):
            raise ValueError("El código del curso ya existe")

        course_id = self._generate_unique_id()

        self._courses[course_id] = Course(course_id, name, code, instructor_id)

        instructor = self._users[instructor_id]
        instructor.add_course(course_id)

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
            return student.enroll_course(course_id)

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

    def create_evaluation(self, course_id, name, evaluation_type, max_score):
        if course_id not in self._courses:
            raise ValueError("El curso no existe")

        if evaluation_type not in ["exam", "assignment"]:
            raise ValueError("Tipo de evaluación no válido")

        evaluation_id = self._generate_unique_id()

        self._evaluations[evaluation_id] = Evaluation(evaluation_id, course_id, name, evaluation_type, max_score)

        course = self._courses[course_id]
        course.add_evaluation(evaluation_id)

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