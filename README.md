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

##Запуск:
py manage.py runserver
