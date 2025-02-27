import uvicorn
from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine
from pydantic import BaseModel

# Конфигурация подключения к базе данных
db_username = 'postgres'  # имя пользователя PostgreSQL
db_password = 'admin'  # пароль
server_name = 'localhost'  # сервер PostgreSQL (или его IP)
db_port = '5432'  # порт по умолчанию для PostgreSQL
db_name = 'Practice_Bot'  # название базы данных

# Строка подключения для PostgreSQL
db_url = f"postgresql+psycopg2://{db_username}:{db_password}@{server_name}:{db_port}/{db_name}"
engine = create_engine(db_url)

app = FastAPI()

class Base(DeclarativeBase): pass

# Модель таблицы teachers
class Teachers(Base):
    __tablename__ = "teachers"

    id_teacher = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tsurname = Column(String(100), nullable=False)
    tname = Column(String(100), nullable=False)
    tpatronymic = Column(String(100), nullable=False)
    tnickname = Column(String(50), unique=True, nullable=False)

# Модель таблицы groups
class Groups(Base):
    __tablename__ = "groups"

    id_group = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gname = Column(String(50), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id_teacher'), nullable=False)

# Модель таблицы students
class Students(Base):
    __tablename__ = "students"

    id_student = Column(Integer, primary_key=True, index=True, autoincrement=True)
    stsurname = Column(String(100), nullable=False)
    stname = Column(String(100), nullable=False)
    stpatronymic = Column(String(100), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id_group'), nullable=False)

Base.metadata.create_all(bind=engine)

# Pydantic-схемы для вывода данных

class TeacherResponse(BaseModel):
    id: int
    surname: str
    name: str
    patronymic: str
    nickname: str

    class Config:
        orm_mode = True

class GroupResponse(BaseModel):
    id: int
    name: str
    teacher_id: int  # Добавлено поле teacher_id

    class Config:
        orm_mode = True

class StudentResponse(BaseModel):
    id: int
    surname: str
    name: str
    patronymic: str
    group_id: int

    class Config:
        orm_mode = True

# Маршруты для работы с таблицей Teachers

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/getTeacher/{id}", response_model=TeacherResponse)
async def get_teacher(id: int):
    with Session(autoflush=False, bind=engine) as db:
        teacher = db.query(Teachers).filter(Teachers.id_teacher == id).first()
        if teacher:
            return TeacherResponse(
                id=teacher.id_teacher,
                surname=teacher.tsurname,
                name=teacher.tname,
                patronymic=teacher.tpatronymic,
                nickname=teacher.tnickname
            )
        return {"message": "Teacher not found"}

@app.get("/getAllTeachers", response_model=list[TeacherResponse])
async def get_all_teachers():
    with Session(autoflush=False, bind=engine) as db:
        teachers = db.query(Teachers).all()
        return [
            TeacherResponse(
                id=teacher.id_teacher,
                surname=teacher.tsurname,
                name=teacher.tname,
                patronymic=teacher.tpatronymic,
                nickname=teacher.tnickname
            ) for teacher in teachers
        ]

# Маршруты для работы с таблицей Groups

@app.get("/getGroup/{id}", response_model=GroupResponse)
async def get_group(id: int):
    with Session(autoflush=False, bind=engine) as db:
        group = db.query(Groups).filter(Groups.id_group == id).first()
        if group:
            return GroupResponse(
                id=group.id_group,
                name=group.gname,
                teacher_id=group.teacher_id  # Возвращаем teacher_id
            )
        return {"message": "Group not found"}

@app.get("/getAllGroups", response_model=list[GroupResponse])
async def get_all_groups():
    with Session(autoflush=False, bind=engine) as db:
        groups = db.query(Groups).all()
        return [
            GroupResponse(
                id=group.id_group,
                name=group.gname,
                teacher_id=group.teacher_id  # Возвращаем teacher_id
            ) for group in groups
        ]

# Маршруты для работы с таблицей Students

@app.get("/getStudent/{id}", response_model=StudentResponse)
async def get_student(id: int):
    with Session(autoflush=False, bind=engine) as db:
        student = db.query(Students).filter(Students.id_student == id).first()
        if student:
            return StudentResponse(
                id=student.id_student,
                surname=student.stsurname,
                name=student.stname,
                patronymic=student.stpatronymic,
                group_id=student.group_id
            )
        return {"message": "Student not found"}

@app.get("/getAllStudents", response_model=list[StudentResponse])
async def get_all_students():
    with Session(autoflush=False, bind=engine) as db:
        students = db.query(Students).all()
        return [
            StudentResponse(
                id=student.id_student,
                surname=student.stsurname,
                name=student.stname,
                patronymic=student.stpatronymic,
                group_id=student.group_id
            ) for student in students
        ]

# Запуск сервера:
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
