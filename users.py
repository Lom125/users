# испортируем модули стандартнй библиотеки uuid
import uuid

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

# создаем соединение к базе данных
engine = sa.create_engine(DB_PATH)
# создаем фабрику сессию
Sessions = sessionmaker(engine)
# создаем сессию
session = Sessions()

# список всех имен таблиц в базе данных
# print(engine.table_names())

class User(Base):
    """
    Опиывает структуру таблицы user для хранения записей музыкальной библиотеки
    """
    # указываем имя таблицы
    __tablename__ = "user"
    # Задаем колонки в формате
    # название_колонки = sa.Column(ТИП_КОЛОНКИ)
    # идентификатор строки
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
	# Пол
    gender = sa.Column(sa.Text)
	# адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # Дата рождения
    birthdate = sa.Column(sa.Text)
    # Рост
    height = sa.Column(sa.REAL)

def email_adr(mail):
    if "@" in mail:
        dom = mail[mail.find("@")+1:]
        if "@" in dom:
            return False
        elif "." in dom:
            return True
        else:
            return False
    else:
        return False

def valid_date(str_date):
    if "-" in str_date:
        dat = str_date.split("-")
        if (len(dat) == 3 and len(dat[0].strip()) == 4):
            if len(dat[1].strip()) == 2 and len(dat[2].strip()) == 2:
                return True
            else:
                return False    
        else:
            return False 
    else:
        return False

def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введите своё имя: ")
    last_name = input("Теперь фамилию: ")
    gender = input("Пол: ")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    while not email_adr(email):
        email = input("Введите правильный адрес электронной почты: ")
    birthdate = input("Дата рождения в формате: ГГГГ-ММ-ДД: ")
    while not valid_date(birthdate):
        birthdate = input("Введите дату в формате: ГГГГ-ММ-ДД: ")
    height = input("Ваш рост в метрах: ")

    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    # возвращаем созданного пользователя
    return user

user = request_data()
session.add(user)
all_users_list = session.query(User).all()
print('Все атлеты')
for user in all_users_list:
    print(user.id, ' Имя: ', user.first_name, ' Фамилия: ', user.last_name, ' Рост: ', user.height, ' Дата рождения: ', user.birthdate)
session.commit()