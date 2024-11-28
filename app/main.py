from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
import psycopg2 
from psycopg2.extras import RealDictCursor

class Student(BaseModel):
    surname: str
    firstname: str
    studentId: str
    bornDate: str
    className: str 


app = FastAPI()

while True:

    try:
        con = psycopg2.connect(database="schoolmanagement", user="postgres",
                            password="root", port="5433", cursor_factory=RealDictCursor)
        cursor = con.cursor()
        print("connection to database successfull")
        break;
    except Exception as error:
        print("connection to database failed")
        print(error)


@app.get("/")
def welcome():
    return {"message": "Welcome"}

# get all students from databases

@app.get("/students")
def getAllStudents():
    cursor.execute(""" SELECT * FROM students """)
    students = cursor.fetchall()

    return {"data": students}

# get a student by his student_id
@app.get("/students/{studentId}")
def getSingleStudent(studentId: str):
    cursor.execute(""" SELECT * FROM students WHERE student_id = %s """,(studentId, ))
    student = cursor.fetchone()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "No student found for this id"})
    
    return {"data": student}

#  create a student 

@app.post("/students", status_code=status.HTTP_201_CREATED)
def createStudent(student: Student):
    print(student.bornDate.strip())
    try:
        formatedBornDate = datetime.strptime(student.bornDate.strip(), '%d-%m-%Y')

        cursor.execute(""" INSERT INTO students (surname, firstname, born_date, class_name, student_id) 
                VALUES (%s, %s, %s, %s, %s ) RETURNING * """, (student.surname.upper(), student.firstname, formatedBornDate, 
                                                               student.className, student.studentId.upper(), ))
        student = cursor.fetchall()
        con.commit()
        print("creation successfull")
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= {"error": "An error occurs during the student creation "})
   
    return {"message": "Student created sucessfully", "data": student}

# update Student

@app.put("/students/")
def updateStudent(student: Student):

    formatedBornDate = datetime.strptime(student.bornDate.strip(), '%d-%m-%Y')
    cursor.execute(""" UPDATE students SET surname = %s ,firstname = %s , born_date = %s , class_name = %s WHERE student_id = %s RETURNING * """, 
                (student.surname, student.firstname, formatedBornDate, student.className, student.studentId.upper(), ))
    updatedStudent = cursor.fetchone()
    if updatedStudent == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error":f"No student with id {student.studentId.upper()} found"})
    
    con.commit()

    return {"message": f"Student with id: {student.studentId.upper()} updated successfully", "data": updatedStudent}

@app.delete("/students/{studentId}")
def deleteStudent(studentId: str):
    try: 
        cursor.execute(""" DELETE FROM students WHERE student_id = %s """, (studentId.upper(), ))
        con.commit()
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": "an error occured"})

    return {"message": f"student {studentId.upper()} deleted successfully"}

