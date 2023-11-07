from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Course, Registration


import click
from sqlalchemy import create_engine

# Your SQLAlchemy code goes here
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


@click.group()
def main():
    pass

@main.command()
def add_student():
    sn = click.prompt("Enter student number")
    existing_student = session.query(Student).filter_by(sn=sn).first()
    if existing_student:
        print(f"Student with sn {sn} already exists. Use a different sn.")
        return
    
    first = click.prompt("Enter first name")
    last = click.prompt("Enter last name")
    gender = click.prompt("Enter gender (m/f)")
    age = click.prompt("Enter age")
    
    student = Student(int(sn), first, last, gender, int(age))
    session.add(student)
    session.commit()
    print("Student added successfully")

# Add more commands for other operations, like adding courses or registrations

if __name__ == "__main__":
    main()

