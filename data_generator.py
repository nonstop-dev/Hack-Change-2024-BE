import json
import random
from datetime import datetime

from nickname_generator import generate

# Списки возможных значений для каждого поля
women_names = ['София', 'Анна', 'Мария', 'Ева', 'Виктория', 'Светлана', 'Ольга', 'Татьяна', 'Наталия', 'Елена']
men_names = ['Артем', 'Александр', 'Михаил', 'Матвей', 'Максим', 'Иван', 'Николай', 'Павел', 'Сергей', 'Егор']
women_last_names = ['Иванова', 'Петрова', 'Сидорова', 'Кузнецова', 'Николаева', 'Михайлова', 'Андреева', 'Волкова', 'Соколова', 'Кравцова']
men_last_names = ['Иванов', 'Петров', 'Сидоров', 'Кузнецов', 'Николаев', 'Михайлов', 'Андреев', 'Волков', 'Соколов', 'Кравцов']

roles = ['Разработчик', 'Тестировщик', 'Дизайнер', 'Менеджер', 'Аналитик']
teams = ['Нытики', 'Координаторы', 'Инноваторы', 'Веб-мастера', 'Бэкендеры']
departments = ['Отдел Счастья', 'Отдел Координации', 'Отдел Инноваций', 'Отдел Веб-технологий', 'Отдел Бэкенда']
cities = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Нижний Новгород', 'Казань', 'Челябинск', 'Омск', 'Самара', 'Ростов-на-Дону']
timezones = ['GMT+03:00', 'GMT+02:00', 'GMT-05:00', 'GMT+08:00', 'GMT+12:00']
skillsSet = ['JavaScript', 'Python', 'Java', 'C++', 'Ruby', 'программирование', 'языки программирования', 'алгоритмы', 'структурные данные', 'алгоритмизация', 'комбинаторика', 'теория графов', 'алгебраические структуры данных', 'криптография', 'базы данных']

def generate_username(full_name):
    first_letter = full_name[0][0]
    three_letters_surname = full_name[-1][:3].rjust(3, 'x')
    number = '{:03d}'.format(random.randrange (1,999))
    username = '{}{}{}'.format(first_letter, three_letters_surname, number)
    return username

def generate_employee():
    is_women = bool(random.getrandbits(1))
    first_name = random.choice(women_names) if is_women else random.choice(men_names)
    last_name = random.choice(women_last_names) if is_women else random.choice(men_last_names)
    name = f"{first_name} {last_name}"
    nickname = generate() #generate_username(translit(name, "ru", reversed=True))
    email = f"{nickname}@mtc.ru"
    role = random.choice(roles)
    team = random.choice(teams)
    department = random.choice(departments)
    project = f"Проект {random.randint(1, 100)}"
    city = random.choice(cities)
    timezone = f"+{random.randint(6, 12):02d}:00"
    skills = ','.join(random.sample(skillsSet, random.randint(1, 6)))
    workHours = f"{random.randint(9, 18):02d}:00-{random.randint(9, 18):02d}:00"
    availability = json.dumps({
        "nextMeeting": f"{datetime.now().hour:02d}:{datetime.now().minute:02d}",
        "currentMeetingEndTime": f"{random.randint(9, 13):02d}:00"
    } if bool(random.getrandbits(1)) else {
        "vacationEndDate": f"{datetime.now().year}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    })

    return {
        'name': name,
        'nickname': nickname,
        'email': email,
        'role': role,
        'team': team,
        'department': department,
        'project': project,
        'city': city,
        'timezone': timezone,
        'skills': skills,
        'workHours': workHours,
        'availability': availability
    }

def generate_employees(count):
    employees = [generate_employee() for _ in range(count)]
    return employees



