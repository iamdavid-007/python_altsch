from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from uuid import UUID

app = FastAPI()


# Define the base model for Student
class StudentBase(BaseModel):
    name: str
    age: int
    sex: str
    height: float


# Define the Student model, which extends the base model with an id
class Student(StudentBase):
    id: UUID


# Define the model for creating a new student, which is the same as the base model
class StudentCreate(StudentBase):
    pass


# Define the model for updating a student, which is the same as the base model
class StudentUpdate(StudentBase):
    pass


# Initialize an empty dictionary to store students
students = {}


# Function to get a student by id
def get_student_by_id(id: str):
    """Get a student by id.

    Args:
        id (str): The id of the student.

    Returns:
        The student if found, else raises a 404 HTTPException.
    """
    if id in students:
        return students[id]
    raise HTTPException(status_code=404, detail="Student not found")


@app.get("/", response_model=dict, status_code=status.HTTP_200_OK)
def read_root():
    """Read the root.

    Returns:
        A welcome message.
    """
    return {"message": "Hello, Welcome to my FastAPI student resource project"}


@app.get("/students", response_model=dict, status_code=status.HTTP_200_OK)
def get_all_students():
    """Get all students.

    Returns:
        A message and a list of all students.
    """
    return {"message": "List of all students", "data": students}


@app.get("/students/{id}", response_model=dict, status_code=status.HTTP_200_OK)
def get_by_id(id: UUID):
    """Get a student by id.

    Args:
        id (UUID): The id of the student.

    Returns:
        A message and the student if found.
    """
    student = get_student_by_id(id)
    return {"message": "Student found", "data": student}


@app.post("/students", response_model=dict, status_code=status.HTTP_201_CREATED)
def add_student(student_in: StudentCreate):
    """Add a student.

    Args:
        student_in (StudentCreate): The student to add.

    Returns:
        A message and the added student.
    """
    student_id = UUID(int=len(students) + 1)
    student = Student(id=student_id, **student_in.dict())
    students[student_id] = student
    return {"message": "Student added successfully", "data": student}


@app.put("/students/{id}", response_model=dict, status_code=status.HTTP_200_OK)
def update_student(id: UUID, student_in: StudentUpdate):
    """Update a student.

    Args:
        id (UUID): The id of the student to update.
        student_in (StudentUpdate): The updated student.

    Returns:
        A message and the updated student.
    """
    student = get_student_by_id(id)
    student.name = student_in.name
    student.age = student_in.age
    student.sex = student_in.sex
    student.height = student_in.height
    return {"message": "Student updated successfully", "data": student}


@app.delete("/students/{id}", response_model=dict)
def delete_student(id: UUID):
    """Delete a student.

    Args:
        id (UUID): The id of the student to delete.

    Returns:
        A message indicating the student was deleted.
    """
    student = students.pop(id, None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
