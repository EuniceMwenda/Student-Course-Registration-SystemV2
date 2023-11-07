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
    id = Column(Integer, primary_key=True)
    description = Column(String)

    registrations = relationship("Registration", back_populates="course")

    def __init__(self, id, description):
        self.id = id
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

st1 = Student(1657, "Billy", "Lake", "m", 23)
st2 = Student(1084, "Lisa", "Mwangi", "f", 21)
st3 = Student(1534, "Luke", "Matt", "m", 24)

session.add(st1)
session.add(st2)
session.add(st3)
session.commit()

course = Course(21, "Computer Science")
session.add(course)
session.commit()

C1 = Course(23, "Pharmacy")
C2 = Course(24, "Data Science")
C3 = Course(25, "Economics")

session.add(C1)
session.add(C2)
session.add(C3)
session.commit()

registration = Registration(1657, 23)
session.add(registration)
session.commit()

results = session.query(Registration).all()
print(results)
