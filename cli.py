from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Course, Registration
import argparse

#A command-line parser
parser = argparse.ArgumentParser(description="Student Registration System")

subparsers = parser.add_subparsers(dest="command", help="Available commands")

# Subcommand to add a new student
add_student_parser = subparsers.add_parser("add_student", help="Add a new student")
add_student_parser.add_argument("--sn", type=int, required=True, help="Student number")
add_student_parser.add_argument("--first", required=True, help="First name")
add_student_parser.add_argument("--last", required=True, help="Last name")
add_student_parser.add_argument("--gender", choices=["m", "f"], required=True, help="Gender (m/f)")
add_student_parser.add_argument("--age", type=int, required=True, help="Age")

# Subcommand to add a new course
add_course_parser = subparsers.add_parser("add_course", help="Add a new course")
add_course_parser.add_argument("--description", required=True, help="Course description")

# Subcommand to register a student for a course
register_parser = subparsers.add_parser("register", help="Register a student for a course")
register_parser.add_argument("--student_id", type=int, required=True, help="Student ID")
register_parser.add_argument("--course_id", type=int, required=True, help="Course ID")

# Subcommand to list all students
list_students_parser = subparsers.add_parser("list_students", help="List all students")

# Subcommand to list all courses
list_courses_parser = subparsers.add_parser("list_courses", help="List all courses")

# Subcommand to list student registrations
list_registrations_parser = subparsers.add_parser("list_registrations", help="List student registrations")
list_registrations_parser.add_argument("--student_id", type=int, required=True, help="Student ID")

args = parser.parse_args()

#Existing code for defining models, creating the database, and initializing the session
from sqlalchemy import create_engine, Column, Integer, String, CHAR, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    sn = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    gender = Column(CHAR)
    age = Column(Integer)

    registrations = relationship("Registration", back_populates="student")

    def __init__(self, sn, first, last, gender, age):
        self.sn = sn
        self.firstname = first
        self.lastname = last
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"({self.sn}) ({self.firstname}) ({self.lastname}) ({self.gender}) ({self.age})"

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)

    registrations = relationship("Registration", back_populates="course")

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return f"({self.id}) ({self.description})"

class Registration(Base):
    __tablename__ = 'registrations'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.sn'))
    course_id = Column(Integer, ForeignKey('courses.id'))

    student = relationship("Student", back_populates="registrations")
    course = relationship("Course", back_populates="registrations")

    def __init__(self, student_id, course_id):
        self.student_id = student_id
        self.course_id = course_id

    def __repr__(self):
        return f"({self.id}) ({self.student_id}) ({self.course_id})"

engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

student = Student(1234, "Sandra", "Smith", "f", 20)
session.add(student)
session.commit()

students_data = [
    (1234, "Sandra", "Smith", "f", 20),
    (1657, "Billy", "Lake", "m", 23),
    (1084, "Lisa", "Mwangi", "f", 21),
    (1534, "Luke", "Matt", "m", 24),
]
for sn, first, last, gender, age in students_data:
    student = Student(sn, first, last, gender, age)
    session.add(student)
session.commit()

course = Course( "Computer Science")
session.add(course)
session.commit()

C1 = Course("Pharmacy")
C2 = Course("Macine Learning")
C3 = Course("Economics")


session.add(C1)
session.add(C2)
session.add(C3)
session.commit()

registration = Registration(1657, 23)
session.add(registration)
session.commit()

reg1 = Registration(1084,  25)
reg2 = Registration(1534,  24)

session.add(reg1)
session.add(reg2)
session.commit()


results = session.query(Student, Registration).join(Registration).all()


for student, registration in results:
    print(f"Student: {student.firstname} {student.lastname} ({student.gender}, {student.age} years old)")
    print(f"Course: {registration.course.description}")
    print("")


results = session.query(Course, Registration).join(Registration).all()

for course, registration in results:
    print(f"Course: {course.description}")
    print("Students:")
    for student in course.registrations:
        print(f"{student.student.firstname} {student.student.lastname} ({student.student.gender}, {student.student.age} years old)")
    print("")

# Functions to handle the subcommands
if args.command == "add_student":
    student = Student(args.sn, args.first, args.last, args.gender, args.age)
    session.add(student)
    session.commit()
    print("Student added successfully!")

elif args.command == "add_course":
    course = Course(args.description)
    session.add(course)
    session.commit()
    print("Course added successfully!")

elif args.command == "register":
    registration = Registration(args.student_id, args.course_id)
    session.add(registration)
    session.commit()
    print("Registration completed!")

elif args.command == "list_students":
    students = session.query(Student).all()
    for student in students:
        print(f"Student: {student.firstname} {student.lastname} ({student.gender}, {student.age} years old)")

elif args.command == "list_courses":
    courses = session.query(Course).all()
    for course in courses:
        print(f"Course: {course.description}")

elif args.command == "list_registrations":
    student_id = args.student_id
    student = session.query(Student).filter_by(sn=student_id).first()
    if student:
        registrations = student.registrations
        for registration in registrations:
            print(f"Course: {registration.course.description}")
    else:
        print(f"No student found with ID {student_id}")



if __name__ == "__main__":
    args = parser.parse_args()

