# проект "Родословная"
Родословная - проект по созданию генеалогического древа семьи.

На главной странице можно посмотреть публичные родословные.

После регистрации можно создать своё древо и его опубликовать, добавлять новых членов родословной, их фотографии, описывать их биографию.

Можно просмотреть структуру генеалогического древа.

## Как развернуть проект локально:
**1. Клонировать репозиторий и перейти в него в командной строке:**

`git clone https://github.com/Olmazurova/family_tree.git`

**2. Cоздать и активировать виртуальное окружение:**

- На ОС Linux:

`python3 -m venv .venv`

`source .venv/bin/activate`

`python3 -m pip install --upgrade pip`

- На ОС Windows:

`python -m venv .venv`
  
`source .venv/Scripts/activate`

`python -m pip install --upgrade pip`

**3. Установить зависимости из файла requirements.txt:**

`pip install -r requirements.txt`

**4. Выполнить миграции:**

- На ОС Linux:

`python3 manage.py migrate`

- На ОС Windows:

`python manage.py migrate`

**5. Запустить проект:**

- На ОС Linux:

`python3 manage.py runserver`

- На ОС Windows:

`python manage.py runserver`


_____
Автор проекта: Ольга Мазурова
