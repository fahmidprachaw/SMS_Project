import json

class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        print(f"Name: {self.name}, Age: {self.age}, Address: {self.address}")

class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []

    def add_grade(self, subject, grade):
        if subject in self.courses:
            self.grades[subject] = grade
            print(f"Grade {grade} added for {self.name} in {subject}.")
        else:
            print(f"Cannot assign grade. {self.name} is not enrolled in {subject}.")

    def enroll_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
            print(f"{self.name} enrolled in {course}.")
        else:
            print(f"{self.name} is already enrolled in {course}.")

    def display_student_info(self):
        self.display_person_info()
        print(f"Student ID: {self.student_id}")
        print(f"Enrolled Courses: {', '.join(self.courses)}")
        print(f"Grades: {self.grades}")

class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)
            print(f"{student.name} enrolled in {self.course_name} (Code: {self.course_code}).")
        else:
            print(f"{student.name} is already enrolled in {self.course_name}.")

    def display_course_info(self):
        print(f"Course Name: {self.course_name}, Code: {self.course_code}, Instructor: {self.instructor}")
        print("Enrolled Students:", ", ".join([student.name for student in self.students]))

class StudentManagementSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def add_student(self):
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        address = input("Enter Address: ")
        student_id = input("Enter Student ID: ")
        if student_id not in self.students:
            student = Student(name, age, address, student_id)
            self.students[student_id] = student
            print(f"Student {name} (ID: {student_id}) added successfully.")
        else:
            print("Student ID already exists.")

    def add_course(self):
        course_name = input("Enter Course Name: ")
        course_code = input("Enter Course Code: ")
        instructor = input("Enter Instructor Name: ")
        if course_code not in self.courses:
            course = Course(course_name, course_code, instructor)
            self.courses[course_code] = course
            print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.")
        else:
            print("Course code already exists.")

    def enroll_student_in_course(self):
        student_id = input("Enter Student ID: ")
        course_code = input("Enter Course Code: ")
        student = self.students.get(student_id)
        course = self.courses.get(course_code)
        if student and course:
            student.enroll_course(course.course_name)
            course.add_student(student)
        else:
            print("Invalid Student ID or Course Code.")

    def add_grade_for_student(self):
        student_id = input("Enter Student ID: ")
        course_code = input("Enter Course Code: ")
        grade = input("Enter Grade: ")
        student = self.students.get(student_id)
        course = self.courses.get(course_code)
        if student and course:
            student.add_grade(course.course_name, grade)
        else:
            print("Invalid Student ID or Course Code.")

    def display_student_details(self):
        student_id = input("Enter Student ID: ")
        student = self.students.get(student_id)
        if student:
            student.display_student_info()
        else:
            print("Student ID not found.")

    def display_course_details(self):
        course_code = input("Enter Course Code: ")
        course = self.courses.get(course_code)
        if course:
            course.display_course_info()
        else:
            print("Course Code not found.")

    def save_data(self):
        data = {
            "students": {sid: {"name": student.name, "age": student.age, "address": student.address,
                               "grades": student.grades, "courses": student.courses}
                         for sid, student in self.students.items()},
            "courses": {cid: {"course_name": course.course_name, "instructor": course.instructor,
                              "students": [s.student_id for s in course.students]}
                        for cid, course in self.courses.items()}
        }
        with open("data.json", "w") as f:
            json.dump(data, f)
        print("All student and course data saved successfully.")

    def load_data(self):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
            self.students = {sid: Student(sdata["name"], sdata["age"], sdata["address"], sid)
                             for sid, sdata in data["students"].items()}
            self.courses = {cid: Course(cdata["course_name"], cid, cdata["instructor"])
                            for cid, cdata in data["courses"].items()}
            for sid, sdata in data["students"].items():
                self.students[sid].grades = sdata["grades"]
                self.students[sid].courses = sdata["courses"]
            for cid, cdata in data["courses"].items():
                for sid in cdata["students"]:
                    self.courses[cid].add_student(self.students[sid])
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No data file found.")

    def run(self):
        while True:
            print("\n==== Student Management System ====")
            print("1. Add New Student")
            print("2. Add New Course")
            print("3. Enroll Student in Course")
            print("4. Add Grade for Student")
            print("5. Display Student Details")
            print("6. Display Course Details")
            print("7. Save Data to File")
            print("8. Load Data from File")
            print("0. Exit")
            option = input("Select Option: ")

            if option == "1":
                self.add_student()
            elif option == "2":
                self.add_course()
            elif option == "3":
                self.enroll_student_in_course()
            elif option == "4":
                self.add_grade_for_student()
            elif option == "5":
                self.display_student_details()
            elif option == "6":
                self.display_course_details()
            elif option == "7":
                self.save_data()
            elif option == "8":
                self.load_data()
            elif option == "0":
                print("Exiting Student Management System. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    sms = StudentManagementSystem()
    sms.run()
