# backend_task_2
## Создать виртуальное окружение:

winows:
py -m venv env

linux:
python3 -m venv env

## Активировать виртуальное окружение:

windows:
.\env\Scripts\activate

linux:
source env/bin/activate

## Установить зависимости:
pip install -r requirements.txt

## База данных

Если уже есть установленный Postgres - пропустить каманду с докером и настроить settings.py под себя.
Если нету Postgres, но есть Docker - выполнить команду:

docker-compose up -d --build

ИЛИ раскоментировать в settings.py базу SQLite и наоборот закомментировать Postgres, тогда устанавливать ничего не нужно.

## Сделать миграции:

py manage.py makemigrations

py manage.py migrate

## Запуск:

py manage.py runserver
(python3 для linux)


# Технологии:
DRF, Docker, PostgreSQL, Pandas

# Как проверять с помощью POSTMAN:

### POST запрос на адрес http://127.0.0.1:8000/api/load

Можно отправить 2 файла сразу, обработаются в правильном порядке.  Выбрать Body -> выбрать form-data -> указать ключ-значение (KEY указать как file; VALUE - выбрать сам файл в постмане)

### GET запрос с фильтрами

http://127.0.0.1:8000/api/org?org=OOO%20Client2Org1&client=client2

%20 - обозначение пробела

org = название организации полностью

client = имя клиента полностью

### GET эндпоинт со списком клиентов (без фильтров)
http://127.0.0.1:8000/api/client


