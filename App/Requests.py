import requests

while True:
    choise = int(input("Выберите с кем работать будем (1)Учителя (2)Группы (3)Студенты: "))

    if choise == 1:
        choise = int(input("Выберите действие с Учителями (1)Get одного учителя (2)Get всех учителей: "))

        if choise == 1:
            teacher_id = int(input("Введите id учителя: "))
            r = requests.get(f'http://127.0.0.1:8000/getTeacher/{teacher_id}')
            print(r.content)
            print(r.status_code)
        elif choise == 2:
            r = requests.get(f'http://127.0.0.1:8000/getAllTeachers')
            print(r.content)
            print(r.status_code)

    elif choise == 2:
        choise = int(input("Выберите действие с Группами (1)Get одной группы (2)Get всех групп: "))

        if choise == 1:
            group_id = int(input("Введите id группы: "))
            r = requests.get(f'http://127.0.0.1:8000/getGroup/{group_id}')
            print(r.content)
            print(r.status_code)
        elif choise == 2:
            r = requests.get(f'http://127.0.0.1:8000/getAllGroups')
            print(r.content)
            print(r.status_code)

    elif choise == 3:
        choise = int(input("Выберите действие со Студентами (1)Get одного студента (2)Get всех студентов: "))

        if choise == 1:
            student_id = int(input("Введите id студента: "))
            r = requests.get(f'http://127.0.0.1:8000/getStudent/{student_id}')
            print(r.content)
            print(r.status_code)
        elif choise == 2:
            r = requests.get(f'http://127.0.0.1:8000/getAllStudents')
            print(r.content)
            print(r.status_code)