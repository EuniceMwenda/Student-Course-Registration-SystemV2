import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Course, Registration

# Create a new student
sn = input("Enter student number: ")
first_name = input("Enter first name: ")
last_name = input("Enter last name: ")
gender = input("Enter gender (m/f): ")
age = input("Enter age: ")

# Initialize the database connection and session
engine = sqlalchemy.create_engine('sqlite:///student_course.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Add the student to the database
student = Student(sn=sn, firstname=first_name, lastname=last_name, gender=gender, age=age)
session.add(student)
session.commit()

print("Student added successfully.")
