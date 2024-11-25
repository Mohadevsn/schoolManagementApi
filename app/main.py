from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import date

class Student(BaseModel):
    surname: str
    firstname: str
    studentId: str
    bornDate: str
    className: str 


app = FastAPI()

students = [
    {
        "studentId": "20220AXTJ",
        "surname": "WADE",
        "firstname": "Mohamed",
        "bornDate": "11/11/2002",
        "className": "GLSI A"
    }
]

def findStudentById(id):
    for std in students:
        if std["studentId"] == id.upper():
            return std

def findStudentIndex(student):
    print(student)
    for i, std in enumerate(students):
        if std["studentId"] == student["studentId"].upper():
            return i
    return None


@app.get("/")
def welcome():
    return {"message": "Welcome"}

@app.get("/students")
def getAllStudents():
    return {"data": students}

@app.get("/students/{studentId}")
def getSingleStudent(studentId: str):
    student = findStudentById(studentId.upper())
    print(student)

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "No student found for this id"})
    
    return {"data": student}


@app.post("/students", status_code=status.HTTP_201_CREATED)
def createStudent(student: Student):
    studentDict = student.model_dump()
    print(studentDict)
    students.append(studentDict)
    return {"data": studentDict}

@app.put("/students")
def updateStudent(student: Student):
    studentIndex = findStudentIndex(student.model_dump())
    print(studentIndex)

    if studentIndex == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":f"No User found for the id: {student.studentId.upper()}"})
    
    students[studentIndex] = student
    return {"message": f"Student with id: {student.studentId.upper()} updated successfully"}

@app.delete("/students/{studentId}")
def deleteStudent(studentId: str):
    student = findStudentById(studentId)

    if student == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": f"No student found for id : {studentId.upper()}"})
    

    studentIndex = findStudentIndex(student)
    students.pop(studentIndex)
    return {"message": f"student {studentId.upper()} deleted successfully"}

